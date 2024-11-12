import sys

import pandas as pd
import ast
import json


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


def cf_to_label(row):

    try:
        labels = []
        threshold = 0.7
        for cf in row:
            if cf > threshold:
                labels.append(1)
            else:
                labels.append(0)

        return labels

    except Exception as e:
        return [0, 0, 0]


def get_certainty_factors(row):

    try:
        cf_list = ast.literal_eval(row)

        gender, race, religion = map(list, zip(*[(x['gender'], x['race'], x['religion']) for x in cf_list]))

        labels = [gender, race, religion]
        results = []

        for array in labels:
            aggregated_cf = 0
            for cf in array:

                if aggregated_cf >= 0 and cf >= 0:
                    # Both positive rule
                    aggregated_cf = aggregated_cf + cf - (aggregated_cf * cf)
                elif aggregated_cf <= 0 and cf <= 0:
                    # Both negative rule
                    aggregated_cf = aggregated_cf + cf + (aggregated_cf * cf)
                else:
                    # Different signs rule
                    aggregated_cf = (aggregated_cf + cf) / (1 - min(abs(aggregated_cf), abs(cf)))

            results.append(aggregated_cf)

        return results

    except Exception as e:
        return 0


if __name__ == '__main__':

    movielens = pd.read_csv("movielens_biasmeter_labeled_paper-evaluation-metric.csv", encoding="utf-8")

    movielens['cf'] = movielens['biasmeter_results'].apply(lambda x: get_certainty_factors(x))

    movielens['labels'] = movielens['cf'].apply(lambda x: cf_to_label(x))

    movielens[['gender', 'race', 'religion']] = pd.DataFrame(movielens['labels'].to_list(), index=movielens.index)

    write_model_labels("results/movielens-1m_biasmeter_gender", movielens[['MovieID', 'gender']])
    write_model_labels("results/movielens-1m_biasmeter_race", movielens[['MovieID', 'race']])
    write_model_labels("results/movielens-1m_biasmeter_religion", movielens[['MovieID', 'religion']])

    goodreads = pd.read_csv("goodreads_biasmeter_labeled_paper-evaluation-metric.csv", encoding="utf-8")

    goodreads['cf'] = goodreads['biasmeter_results'].apply(get_certainty_factors)

    goodreads['labels'] = goodreads['cf'].apply(cf_to_label)

    goodreads[['gender', 'race', 'religion']] = pd.DataFrame(goodreads['labels'].to_list(), index=goodreads.index)

    write_model_labels("results/goodreads_biasmeter_gender", goodreads[['book_id', 'gender']])
    write_model_labels("results/goodreads_biasmeter_race", goodreads[['book_id', 'race']])
    write_model_labels("results/goodreads_biasmeter_religion", goodreads[['book_id', 'religion']])