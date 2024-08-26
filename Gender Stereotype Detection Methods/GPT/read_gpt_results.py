import json
import re
import sys

import pandas as pd
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read jsonfiles and write the labels to a csv file')
    parser.add_argument('--dataset', type=str, help='The dataset to analyse. Either ml or gr', required=True)

    args = parser.parse_args()
    dataset = args.dataset
    json_results = []
    with open(f"results/sdm_results_{dataset}.jsonl", "r") as f:

        for line in f:
            json_results.append(json.loads(line))

    gpt_labels = {}
    output_ = {}
    labels = []
    for json_obj in json_results:
        try:
            input = json_obj[0]
            output = json_obj[1]
            metadata = json_obj[2]
            response = output['choices'][0]['message']['content']
            output_[int(metadata['id'])] = response


        except Exception as e:
            continue
    structured_data = {}

    for key, value in output_.items():
        lines = value.split("\n")
        temp_dict = {}

        for line in lines:
            line = line.lower()
            match = re.search(r'stereotype: (.+), probability:? ([0-9]+(\.[0-9]+)?)(\.|$)', line)

            if match:
                stereotype = match.group(1)
                probability = float(match.group(2))
                temp_dict[stereotype] = probability

        if temp_dict:
            structured_data[key] = temp_dict
        else:
            structured_data[key] = 0

    labels_gpt35 = dict(sorted(structured_data.items()))
    print(structured_data)
    print(labels_gpt35)

    labels_df = pd.DataFrame.from_dict(labels_gpt35, orient='index').reset_index()
    labels_df.columns = ['movie_id', 'labels']


    print(len(labels_gpt35))
    print("#"*50)
    
    print("Length of all labels:")
    num_categorized_items = len(labels_gpt35)
    print(len(labels_gpt35))
    print()
    labels_gpt35 = {k: v for k, v in labels_gpt35.items() if v != 0}
    
    print("Length of stereotype labels:")
    print(len(labels_gpt35))
    print()
    
    stereotype_df = pd.DataFrame(list(labels_gpt35.items()), columns=["id", "label"])

    stereotype_df['stereotype'] = stereotype_df['label'].apply(lambda x: list(x.keys())[0])
    stereotype_df['probability'] = stereotype_df['label'].apply(lambda x: list(x.values())[0])
    stereotype_df.drop(columns=['label'], inplace=True)
    
    stereotype_df = stereotype_df[stereotype_df['probability'] >= 0.7]
    print("#"*50)
    print(f"Length of all labels: {num_categorized_items}")
    print("Length of stereotype labels")
    num_gender = len(stereotype_df[stereotype_df['stereotype'] == 'gender'])
    num_race = len(stereotype_df[stereotype_df['stereotype'] == 'race'])
    num_religion = len(stereotype_df[stereotype_df['stereotype'] == 'religion'])
    
    print(f"Gender:  {num_gender}; Proportion: {num_gender / num_categorized_items:.4f}")
    print(f"Race: {num_race}; Proportion: {num_race / num_categorized_items:.4f}")
    print(f"Religion: {num_religion}; Proportion: {(num_religion / num_categorized_items):.4f}")
    save_df = stereotype_df.copy()
    save_df['label'] = 1
    save_df.drop(columns=['probability'], inplace=True)
    ds = "movielens-1m" if dataset == 'ml' else "goodreads"
    for stereotype in ['gender', 'race', 'religion']:
        stereotype_df[stereotype_df['stereotype'] == stereotype].drop(columns=['stereotype']).to_csv(f"results/{ds}_gpt_{stereotype}.csv", index=False)
    


