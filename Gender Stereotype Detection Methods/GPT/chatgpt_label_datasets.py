import sys
import os
import json
import pandas as pd


def create_input_file(data, filename_cp, type_of_item):
    
        
    input_prompt = "Instruction: You are an expert assessor who is tasked with identifying stereotypes in pieces of text. " \
                f"The text are descriptions of certain {type_of_item} \n." \
                "The texts are a few sentences long and if a stereotype is present output the stereotype label and a numbered probability estimation of its presence in that text. " \
                "The stereotype can have one of the following labels: \n" \
                "1. Gender\n" \
                "2. Race\n" \
                "3. Religion\n\n" \
                "Please adhere to the following output format and do not include anything else if a stereotype is present:\n" \
                "Stereotype: {stereotype label}, Probability: {the numbered probability as a probability between 0 and 1}\n" \
                "If the stereotype is not present output: \n" \
                "0 \n\n" \
                "Please provide your assessment for the following text: \n"
    if dataset == 'ml':
        jobs = []

        for index, row in data.iterrows():
            jobs.append({
                "model": "gpt-3.5-turbo" if gpt_version == '' else "gpt-4",
                "messages": [
                    {"role": "system", "content": input_prompt},
                    {"role": "user", "content": f"{row['description']}\n"}
                ],
                "metadata": {"id": row['id']}
            })

        if os.path.exists(filename_cp):
            os.remove(filename_cp)
        with open(filename_cp , "w") as f:
            for job in jobs:
                json_string = json.dumps(job)
                f.write(json_string + "\n")
    if dataset == 'gr':
        jobs = {}
        batch_size = 9950
        print(len(data))
        for index, row in data.iterrows():
            batch = int(index // batch_size)

            jobs.setdefault(batch, []).append({
                "model": "gpt-3.5-turbo" if gpt_version == '' else "gpt-4",
                "messages": [
                    {"role": "system", "content": input_prompt},
                    {"role": "user", "content": f"{row['description']}\n"}
                ],
                "metadata": {"id": row['id']}
            })
        for batch, jobs in jobs.items():
            if os.path.exists(filename_cp + str(batch) + '.jsonl'):
                os.remove(filename_cp + str(batch) + '.jsonl')
            with open(filename_cp + str(batch) + '.jsonl', "w") as f:
                for job in jobs:
                    json_string = json.dumps(job)
                    f.write(json_string + "\n")
                    
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create jsonl file for GPT-3.5-turbo or GPT-4 input for stereotype detection')
    parser.add_argument('--dataset', type=str, help='The dataset to create the input for. Either ml or gr', required=True)
    parser.add_argument('--gpt_version', type=str, help='The version of GPT to use. Either 3.5 or 4', required=False)
    
    args = parser.parse_args()
    gpt_version = args.gpt_version if args.gpt_version is not None else ''
    dataset = args.dataset
    
    if dataset == 'ml':
        filename_cp = f"data/jobs_ml{gpt_version}.jsonl"
        data = pd.read_csv("data/ml_descriptions_processed.csv")
        type_of_item = "movies"
    if dataset == 'gr':
        filename_cp = f"data/jobs_gr{gpt_version}_"
        data = pd.read_csv("../data/gr_descriptions_processed.csv")
        type_of_item = "books"
        
    create_input_file(data, filename_cp, type_of_item)