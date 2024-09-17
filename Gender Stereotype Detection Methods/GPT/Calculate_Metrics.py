import json
import os
import math
import numpy as np
import sys

import pandas as pd
import glob

from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import ttest_rel
import seaborn as sns
import matplotlib.pyplot as plt


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
    names = [os.path.basename(x) for x in all_files]
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
                labels.append(1 if row in st_labels else 0)
                #labels.append(st_labels.get(str(row), 0))
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


def plot_metric_ttest(metric_df, metric_name, side_info):
    """"
    This method calculates and plots the paired t-test.

    Parameters
    ----------
    metric_df: Dataframe with all rec models and their stereotype metric scores
    metric_name: Name of the metric for the plot
    side_info: Side information for the dataset

    """

    # Get the names of all the models (columns except the 'UserID' column)
    rec_models = [col for col in metric_df.columns if col != 'UserID']

    # Create an empty DataFrame to store p-values
    p_value_matrix = pd.DataFrame(index=rec_models, columns=rec_models)
    columns = []
    # Run paired t-tests for each pair of models
    for i, model1 in enumerate(rec_models):
        columns.append(model1)
        for j, model2 in enumerate(rec_models):
            # Get the lists of hits for both models
            scores1 = metric_df[model1]
            scores2 = metric_df[model2]

            if model1 == model2:
                # Store the p-value in the matrix
                p_value_matrix.loc[model1, model2] = 1

            else:
                # Run the paired t-test
                _, p_value = ttest_rel(scores1, scores2)

                # Store the p-value in the matrix
                p_value_matrix.loc[model1, model2] = p_value

    # Replace NaN values with 1
    p_value_matrix[pd.isna(p_value_matrix)] = 1

    # Convert potential string values to float
    p_value_matrix = p_value_matrix.astype(float)

    #print(p_value_matrix)
    p_value_matrix = p_value_matrix.reindex(index=columns, columns=columns)
    print(p_value_matrix.applymap(lambda x: round(x, 3)))

    # Set the threshold
    threshold = 0.05

    # Bonferroni correction
    threshold = threshold / len(rec_models)

    # Create a mask array for values greater than or equal to the threshold
    above_threshold_mask = p_value_matrix >= threshold

    # Create a mask array for values less than the threshold
    below_threshold_mask = p_value_matrix < threshold

    # Create custom color palettes for red and blue shades
    red_palette = sns.color_palette("Reds", n_colors=5)
    blue_palette = sns.color_palette("Blues", n_colors=5)

    # Reverse the blue palette to have lighter shades at the bottom
    blue_palette = blue_palette[::-1]

    # Create custom color maps using the palettes
    cmap_red = LinearSegmentedColormap.from_list("custom_red", red_palette)
    cmap_blue = LinearSegmentedColormap.from_list("custom_blue", blue_palette)

    # Plot the heatmap using seaborn with the custom color maps
    plt.figure(figsize=(16, 12))

    # All values that are above the threshold are plotted with the red color map, i.e. non-significant values
    sns.heatmap(p_value_matrix, cmap=cmap_red, cbar=False, mask=below_threshold_mask, vmin=threshold, vmax=1)

    # All values that are below the threshold are plotted with the blue color map, i.e. significant values
    sns.heatmap(p_value_matrix, cmap=cmap_blue, cbar=False, mask=above_threshold_mask, vmin=0, vmax=threshold,
                linewidths=0.1, linecolor="black")

    path = f"Results/SDM/{detection_model}/significance/Figures"
    if not os.path.exists(path):
        os.makedirs(path)
    # plt.title(name)
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.savefig(
        f'{path}/{dataset_name}_{side_info}_{detection_model}_{stereotype}_{metric_name}.png')
    #plt.show()


def calc_st_metrics(rec_models_df, model_name, side_info):
    """"
    This method calculates the stereotype metrics for all the rec models in the dataframe.
    Metrics can be easily expanded, look at the code to add them the same way.

    Parameters
    ----------
    rec_models_df: Dataframe with all recommender models as columns with presence of stereotype lists as values

    model_name: Model name from the genesis file

    side_info: Model name from the genesis file

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
              f"Stereotype Model: {detection_model}\n Dataset: {data} {side_info}\n Stereotype: {stereotype}\n "
              f"HITS: {avg_hit_per_user}\n "
              f"MRR_BAD: {avg_mrr_per_user}\n "
              f"REC-ST: {avg_rec_st_per_user}")
        print("################################################")
        print()
        print("------------------------------------------------")
        print()
    path = f"Results/SDM/{detection_model}/significance"
    if not os.path.exists(path):
        os.makedirs(path)
    hits_df.to_csv(
        f"{path}/{dataset_name}_{side_info}_{detection_model}_{stereotype}_HITS.csv",
        index=False)
    mrr_df.to_csv(
        f"{path}/{dataset_name}_{side_info}_{detection_model}_{stereotype}_MRRBAD.csv",
        index=False)
    rec_st_df.to_csv(
        f"{path}/{dataset_name}_{side_info}_{detection_model}_{stereotype}_REC-ST.csv",
        index=False)

    return hits_df, mrr_df, rec_st_df


def calc_presence_st(recommendation_list, st_labels, side_info):
    """"
    This method calculates for each recommendation list the presence of stereotype in the rec_list

    Parameters
    ----------
    recommendation_list: A Recommender model's recommendation list
    st_labels: The model that contains the ids and stereotype labels of the datasets
    side_info: Whether the model contains side-information or not

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
    path = f"Results/SDM/{detection_model}/significance"
    if not os.path.exists(path):
        os.makedirs(path)
    all_models_df.to_csv(
        f"{path}/{dataset_name}_{side_info}_{detection_model}_{stereotype}.csv",
        index=False)

    return all_models_df


import argparse
if __name__ == '__main__':
    #python Calculate_Metrics.py "ml" --models "MostPop,Random,ItemKNN,UserKNN,BPRMF,FunkSVD,MF,PMF,PureSVD,Slim,DeepFM,NeuMF,MultiVAE,AMF,VSM" --stereotype "gender" --fold "0"
    global dataset_name
    parser = argparse.ArgumentParser(description='Compute stereotype metrics on recommendation list.')
    parser.add_argument('dataset_name', type=str, help='Name of the dataset to extract files from.', choices=['gr', 'ml'])
    parser.add_argument('--models', type=str, help='List of models used for recommendation.')
    parser.add_argument('--stereotype', type=str, help='Type of stereotype', choices=['gender', 'race', 'religion'])
    parser.add_argument('--fold', type=int, help='Fold numbert', default=0)
    
    args = parser.parse_args()
    dataset_name = args.dataset_name
    models = args.models
    models = models.split(",")
    fold = int(args.fold)
    
    type_of_stereotype = args.stereotype
    
    stereotype_df = pd.read_csv(f"results/GPT/sdm_results_{dataset_name}.csv")
    
    stereotype_df = stereotype_df[stereotype_df['stereotype'] == type_of_stereotype]
    stereotype_labels = set(stereotype_df["id"])
    
    if dataset_name == "gr":
        # Get the recommendation files
        rec_models = get_recommender_models('recs/goodreads/recs/*.tsv')
    elif dataset_name == "ml":
        # rec_models_movielens_noside = get_recommender_models('Results/movielens/children/nosideinfo/recs/*.tsv')
        rec_models = get_recommender_models(f'recs/movielens/children/sideinfo/fold{fold}/*.tsv')
        
    rec_models = [(name, path) for name, path in rec_models if name in models]
    # rec_models_movielens = [(rec_models_movielens_noside, "no-sideinfo"),
    # (rec_models_movielens_side, "sideinfo")]

    for model in models:
        # Split the names from Genesis (Format is dataset-name_stereotype-detection-model_type-stereotype)
        split = model.split("_")
        data = dataset_name
        detection_model = 'chatgpt'
        stereotype = type_of_stereotype

        if data == "gr":
            dataset_name = "Goodreads"

            #columns = ["MostPop", "Random", "ItemKNN", "UserKNN", "BPRMF", "FunkSVD", "MF", "PMF",
            #           "PureSVD", "Slim",  "DeepFM", "NeuMF", "MultiVAE", "AMF"]

            
            models_df = calc_presence_st(rec_models, stereotype_labels, "")
            
            hits, mrr_bad, rec_sts = calc_st_metrics(models_df, model, "")

            plot_metric_ttest(hits, "HITS", "")
            plot_metric_ttest(mrr_bad, "MRR_BAD", "")
            plot_metric_ttest(rec_sts, "REC-ST", "")

        elif data == "ml":
            dataset_name = "ML-children"

            #columns = ["MostPop", "Random", "ItemKNN", "UserKNN", "BPRMF", "FunkSVD", "MF", "PMF",
            #           "PureSVD", "Slim",  "DeepFM", "NeuMF", "MultiVAE", "AMF", "VSM"]

            
            models_df = calc_presence_st(rec_models, stereotype_labels, f"fold{fold}")
            hits, mrr_bad, rec_sts = calc_st_metrics(models_df, model, f"fold{fold}")

            plot_metric_ttest(hits, "HITS", f"fold{fold}")
            plot_metric_ttest(mrr_bad, "MRR_BAD", f"fold{fold}")
            plot_metric_ttest(rec_sts, "REC-ST", f"fold{fold}")


