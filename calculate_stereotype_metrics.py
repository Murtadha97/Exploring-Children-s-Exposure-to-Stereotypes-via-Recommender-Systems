import json
import os
import math

import pandas as pd
import glob


def get_recommender_models(file_dir):
    """

    This method gets all recommendation files (.tsv) from a folder.

    Parameters
    ----------
    file_dir: path to directory that has the recommendation files with .tsv extension

    Returns
    -------
    List of tuples of recommendation model name and path to the file

    """
    all_files = glob.glob(file_dir)
    names = [os.path.basename(x).split("_")[0] for x in all_files]
    for i, name in enumerate(names):
        if "." in name:
            names[i] = name.split(".")[0]
    models = list(zip(names, all_files))

    return models


def round_up(num, decimals=3):
    return math.ceil(num * 10 ** decimals) / 10 ** decimals


def calculate_mrr_bad(recommendation_list):
    """"
        This method calculates MRR_BAD score metric for a recommendation list.

        Parameters
        ----------
        recommendation_list: A Recommender model's recommendation list

        Returns
        -------
        The MRR_BAD score
        """

    for r, val in enumerate(recommendation_list, start=1):
        if val == 1:
            return 1 / r

    return 0


def calculate_rec_st(recommendation_list):
    """"
    This method calculates REC-ST score metric (the adapted SERP-MS) for a recommendation list.

    Parameters
    ----------
    recommendation_list: A Recommender model's recommendation list

    Returns
    -------
    The REC-ST score
    """

    n = len(recommendation_list)
    score = 0
    for r, val in enumerate(recommendation_list, start=1):
        score += (val * (n - r + 1))

    # Normalize the scores
    score = score / ((n * (n + 1)) / 2)

    return score


def calculate_hit(recommendation_list):
    """"
    This method calculates if a HIT occurred for a recommendation list.

    Parameters
    ----------
    recommendation_list: A Recommender model's recommendation list

    Returns
    -------
    The HIT score
    """
    # Check if the list contains integers 0 and 1 only
    if not all(x in [0, 1] for x in recommendation_list):
        return "Invalid values in the list. The list should contain only 0s and 1s."

    return 1 if 1 in recommendation_list else 0


def calculate_st_presence_per_model(recommender_file, st_labels):
    """"
    This method calculates if the stereotypes are present per recommendation file
    """

    try:
        recommendations_df = pd.read_csv(recommender_file, sep="\t", header=None, names=["userID", "itemID", "score"])

        grouped_users = recommendations_df.groupby("userID")
        nr_users = recommendations_df["userID"].nunique()

        user_labels = []
        hit = 0

        for user_id, recs in grouped_users:
            labels = []
            for row in recs['itemID'][:10]:
                # Get the stereotype label for the item if it exists, otherwise 0
                labels.append(st_labels.get(str(row), 0))
            user_labels.append({user_id: labels})
            if 1 in labels:
                hit += 1
            # print(labels)

        # Calculate HITS
        avg_hit = math.ceil((hit / nr_users) * 1000) / 1000
        return avg_hit, user_labels

    except Exception as e:
        print(e)


def list_to_df(list_of_dicts, model_name):
    data = {}
    for single_dict in list_of_dicts:
        for k, v in single_dict.items():
            data[k] = v
    temp_df = pd.DataFrame(list(data.items()), columns=['UserID', model_name])
    return temp_df


def calc_st_metrics(rec_models_df, model_name):
    """"
    This method calculates the stereotype metrics for all the rec models in the dataframe.
    Metrics can be easily expanded, look at the code to add them the same way.

    Parameters
    ----------
    rec_models_df: Dataframe with all recommender models as columns with presence of stereotype lists as values

    model_name: Model name from the genesis file

    Returns
    -------
    Returns x amount of dataframes for x amount stereotypes with all rec models.
    """
    hits_df = pd.DataFrame()
    mrr_df = pd.DataFrame()
    rec_st_df = pd.DataFrame()

    # Get the names of all the models (columns except the 'UserID' column)
    rec_models = [col for col in rec_models_df.columns if col != 'UserID']

    hits_df['UserID'] = rec_models_df['UserID']
    mrr_df['UserID'] = rec_models_df['UserID']
    rec_st_df['UserID'] = rec_models_df['UserID']

    for rec_model in rec_models:
        hits_df[rec_model] = rec_models_df[rec_model].apply(calculate_hit)
        mrr_df[rec_model] = rec_models_df[rec_model].apply(calculate_mrr_bad)
        rec_st_df[rec_model] = rec_models_df[rec_model].apply(calculate_rec_st)

        avg_hit_per_user = round_up(hits_df[rec_model].sum() / hits_df['UserID'].nunique(), 3)
        avg_mrr_per_user = round_up(mrr_df[rec_model].sum() / mrr_df['UserID'].nunique(), 3)
        avg_rec_st_per_user = round_up(rec_st_df[rec_model].sum() / rec_st_df['UserID'].nunique(), 3)

        print("################################################")
        print(f"Calculating HITS per user:\n Recommender Model: {rec_model}\n "
              f"Stereotype Model: {detection_model}\n Dataset: {data}\n Stereotype: {stereotype}\n "
              f"HITS: {avg_hit_per_user}\n "
              f"MRR_BAD: {avg_mrr_per_user}\n "
              f"REC-ST: {avg_rec_st_per_user}")
        print("################################################")
        print()
        print("------------------------------------------------")
        print()
    results_dir = f"Results/SDM/{detection_model}/"

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    hits_df.to_csv(f"{results_dir}/{dataset_name}_{detection_model}_{stereotype}_HITS.csv", index=False)

    mrr_df.to_csv(f"{results_dir}/{dataset_name}_{detection_model}_{stereotype}_MRRBAD.csv", index=False)

    rec_st_df.to_csv(f"{results_dir}/{dataset_name}_{detection_model}_{stereotype}_REC-ST.csv", index=False)

    return hits_df, mrr_df, rec_st_df


def calc_presence_st(recommendation_list, st_labels):
    """"
    This method calculates for each recommendation list the presence of stereotype in the rec_list per user

    Parameters
    ----------
    recommendation_list: A Recommender model's recommendation list
    st_labels: The model that contains the ids and stereotype labels of the datasets

    Returns
    -------
    A Dataframe containing the presence of stereotypes per userID for every rec model.
    """
    # Initialize the metric dataframes
    all_models_df = pd.DataFrame()

    for rec_model, path in recommendation_list:
        hit_normalized, presence_per_user = calculate_st_presence_per_model(path, st_labels)

        new_df = list_to_df(presence_per_user, rec_model)

        if all_models_df.empty:
            all_models_df = new_df
        else:
            all_models_df = pd.merge(all_models_df, new_df, on="UserID", how="outer")

    results_dir = f"Results/SDM/{detection_model}/"

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    all_models_df.to_csv(f"{results_dir}/{dataset_name}_{detection_model}_{stereotype}.csv", index=False)

    return all_models_df


if __name__ == '__main__':
    global dataset_name

    # Load Genesis file
    with open('C:\\Users\\murta\\OneDrive - Delft University of Technology\\Thesis-2023\\Gender Stereotype Detection Methods\\genesis.json', "r") as f:
        content = json.loads(f.read())

    # Get the recommendation files
    # rec_models_goodreads = get_recommender_models('input_recommendations/goodreads/*.tsv')
    # rec_models_movielens = get_recommender_models('input_recommendations/movielens/*.tsv')
    rec_models_goodreads = get_recommender_models('C:\\Users\\murta\\OneDrive - Delft University of Technology\\Thesis-2023\\Experiments/Results/goodreads/recs/*.tsv')
    rec_models_movielens = get_recommender_models('C:\\Users\\murta\\OneDrive - Delft University of Technology\\Thesis-2023\\Experiments/Results/movielens/children/sideinfo/fold0/*.tsv')

    for model in content.keys():

        stereotype_labels = content[model]

        # Split the names from Genesis (Format is dataset-name_stereotype-detection-model_type-stereotype)
        split = model.split("_")
        data = split[0]
        detection_model = split[1]
        stereotype = split[2]

        if data == "goodreads":
            dataset_name = "Goodreads"

            columns = ["MostPop", "Random", "ItemKNN", "UserKNN", "BPRMF", "FunkSVD", "MF", "PMF",
                       "PureSVD", "Slim", "ConvMF", "DeepFM", "NeuMF", "MultiVAE", "AMF"]

            models_df = calc_presence_st(rec_models_goodreads, stereotype_labels)

        else:
            dataset_name = "ML-children"

            columns = ["MostPop", "Random", "ItemKNN", "UserKNN", "AttributeItemKNN", "AttributeUserKNN", "BPRMF",
                       "FunkSVD", "MF", "MF2020", "PMF", "PureSVD", "Slim", "ConvMF", "DeepFM", "NeuMF", "MultiVAE",
                       "AMF", "VSM"]

            models_df = calc_presence_st(rec_models_movielens, stereotype_labels)

        hits, mrr_bad, rec_sts = calc_st_metrics(models_df, model)
