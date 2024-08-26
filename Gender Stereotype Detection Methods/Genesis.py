import json


def validate_json_file(file):
    """
        Validate if the json file contains a valid format to be able to use for the experiments and the metrics
    """
    try:
        with open(file) as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return False
            for key, value in data.items():
                if not isinstance(key, str) or not isinstance(value, dict):
                    return False
                for inner_key, inner_value in value.items():
                    if not isinstance(inner_key, str) or not isinstance(inner_value, int):
                        return False
    except (json.JSONDecodeError, FileNotFoundError):
        return False
    return True


def write_model_labels(name, df):
    """
        This method writes a json object with the name of the model as the key
        and as a value a dictionary with MovieIDs as keys and values the label of the stereotype
        name is the name of the model in following format: dataset-name_model-name_stereotype
        df is a dataframe consisting of 2 columns: ItemID and Stereotype Label
    """
    df_to_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
    model = {name: df_to_dict}

    file_path = "genesis.json"

    try:
        # Initialize an empty or existing JSON object
        existing_json = {}

        # Read the file content if the file exists and is not empty
        try:
            with open(file_path, "r") as f:
                content = f.read().strip()
                if content:
                    existing_json = json.loads(content)
        except FileNotFoundError:
            pass  # File doesn't exist yet, will be created in the next step

        # Update the JSON object with new data
        existing_json.update(model)

        # Write the updated JSON back to the file
        with open(file_path, "w") as f:
            json.dump(existing_json, f)

    except Exception as e:
        print(e)

import pandas as pd
if __name__ == '__main__':
    write_model_labels("movielens-1m_biasmeter_gender", pd.read_csv("results/movielens-1m_biasmeter_gender.csv", sep=','))
    write_model_labels("movielens-1m_biasmeter_race", pd.read_csv("results/movielens-1m_biasmeter_race.csv", sep=','))
    write_model_labels("movielens-1m_biasmeter_religion", pd.read_csv("results/movielens-1m_biasmeter_religion.csv", sep=','))
    write_model_labels("movielens-1m_gpt_gender", pd.read_csv("results/movielens-1m_gpt_gender.csv", sep=','))
    write_model_labels("movielens-1m_gpt_race", pd.read_csv("results/movielens-1m_gpt_gender.csv", sep=','))
    write_model_labels("movielens-1m_gpt_religion", pd.read_csv("results/movielens-1m_gpt_religion.csv", sep=','))
    write_model_labels("movielens-1m_ngim_gender", pd.read_csv("results/movielens-1m_ngim_gender.csv", sep=','))
    write_model_labels("goodreads_biasmeter_gender", pd.read_csv("results/goodreads_biasmeter_gender.csv", sep=','))
    write_model_labels("goodreads_biasmeter_race", pd.read_csv("results/goodreads_biasmeter_race.csv", sep=','))
    write_model_labels("goodreads_biasmeter_religion", pd.read_csv("results/goodreads_biasmeter_religion.csv", sep=','))
    write_model_labels("goodreads_gpt_gender", pd.read_csv("results/goodreads_gpt_gender.csv", sep=','))
    write_model_labels("goodreads_gpt_race", pd.read_csv("results/goodreads_gpt_gender.csv", sep=','))
    write_model_labels("goodreads_gpt_religion", pd.read_csv("results/goodreads_gpt_religion.csv", sep=','))
    write_model_labels("goodreads_ngim_gender", pd.read_csv("results/goodreads_ngim_gender.csv", sep=','))
    
    

    