import sys

import pandas as pd
import glob
import os

from matplotlib.colors import LinearSegmentedColormap
from scipy.stats import ttest_rel
import seaborn as sns
import matplotlib.pyplot as plt


def plot_metric_ttest(metric_df, metric_name):
    """"
    This method calculates and plots the paired t-test.

    Parameters
    ----------
    metric_df: Dataframe with all rec models and their stereotype metric scores
    metric_name: Name of the metric for the plot

    """

    # Get the names of all the models (columns except the 'UserID' column)
    rec_models = [col for col in metric_df.columns if col != 'UserID']

    # Create an empty DataFrame to store p-values
    p_value_matrix = pd.DataFrame(index=rec_models, columns=rec_models)

    # Run paired t-tests for each pair of models
    for i, model1 in enumerate(rec_models):
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

    print(p_value_matrix)
    p_value_matrix = p_value_matrix.reindex(index=columns, columns=columns)
    print(p_value_matrix)

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

    # plt.title(name)
    plt.xlabel("")
    plt.ylabel("")
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    results_dir = f"Results/SDM/{st_model}/significance/Figures/"

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    plt.savefig(f"{results_dir}/{os.path.basename(file).split('.')[0]}_significance.png")
    plt.show()


def plot_prominence(metric_df, metric_name):
    """"
    This method plots the metric scores for each recommender.

    Parameters
    ----------
    metric_df: Dataframe with all rec models and their stereotype metric scores
    metric_name: Name of the metric for the plot

    """

    plt.figure(figsize=(16, 12))
    if metric_name == "HITS":
        sns.barplot(data=metric_df, ci=None, palette=palette_datasets)
    else:
        sns.boxplot(data=metric_df, showmeans=True, meanprops={'marker': 'o', 'markerfacecolor': 'white',
                                                               'markeredgecolor': 'black', 'markersize': '8'},
                    palette=palette_datasets)

    if metric_name == "MRRBAD":
        metric_name = r"$MRR_{BAD," + str(st_type) + "}$"

    if metric_name == "HITS":
        metric_name = r"$HIT_{BAD," + str(st_type) + "}$"

    plt.ylabel(metric_name, fontsize=14)
    plt.xlabel('')
    plt.xticks(rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()

    results_dir = f"Results/SDM/{st_model}/prominence/Figures/"

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    plt.savefig(f"{results_dir}/{os.path.basename(file).split('.')[0]}_Boxplot.png")
    plt.show()


columns_goodreads = ["MostPop", "Random", "ItemKNN", "UserKNN", "BPRMF", "FunkSVD", "MF", "PMF",
                     "PureSVD", "Slim", "ConvMF", "DeepFM", "NeuMF", "MultiVAE", "AMF"]

columns_ml = ["MostPop", "Random", "ItemKNN", "UserKNN", "AttributeItemKNN", "AttributeUserKNN", "BPRMF", "FunkSVD",
              "MF", "MF2020", "PMF",
              "PureSVD", "Slim", "ConvMF", "DeepFM", "NeuMF", "MultiVAE", "AMF", "VSM"]

# Define gradients for each type of recommender
blues = sns.color_palette("mako", n_colors=10)  # For Non-Personalized
reds = sns.color_palette("Reds", n_colors=10)  # For Neighborhood
greens = sns.color_palette("Greens", n_colors=10)  # For Latent-Factors
cyans = sns.color_palette("Purples", n_colors=10)  # For Neural
magenta = sns.color_palette("Oranges", n_colors=10)  # For Adversarial
yellow = sns.color_palette("YlOrBr", n_colors=10)  # For Content-Based

palette_datasets = {
    "MostPop": blues[3],
    "Random": blues[4],

    "ItemKNN": reds[3],
    "UserKNN": reds[4],
    "AttributeItemKNN": reds[5],
    "AttributeUserKNN": reds[6],

    "BPRMF": greens[3],
    "FunkSVD": greens[4],
    "MF": greens[5],
    "MF2020": greens[6],
    "PMF": greens[7],
    "PureSVD": greens[8],
    "Slim": greens[9],

    "ConvMF": cyans[3],
    "DeepFM": cyans[4],
    "NeuMF": cyans[5],
    "MultiVAE": cyans[6],

    "AMF": magenta[3],
    "VSM": yellow[1]
}

# List of metrics
metrics = ["_HITS.csv", "_MRRBAD.csv", "_REC-ST.csv"]

base_dir = "Results/SDM/"

# Constructing a list of patterns to match
patterns = [os.path.join(base_dir, '**/*' + metric) for metric in metrics]

print(patterns)

all_files = []

# Iterating over each pattern and adding matching files to the list
for pattern in patterns:
    all_files.extend(glob.glob(pattern, recursive=True))

all_files = list(set(all_files))

# Loop through each metric and plot prominence and significance
for file in all_files:

    print(file)
    split = os.path.basename(file).split("_")
    dataset = split[0]
    st_model = split[1]
    st_type = split[2].capitalize()
    metric = split[3].split(".")[0]

    df = pd.read_csv(file)

    # Drop the 'UserID' column
    df.drop(columns=['UserID'], inplace=True)

    df.rename(columns={"MostPop.tsv": "MostPop"}, inplace=True)

    if dataset == "Goodreads":
        columns = columns_goodreads
        df = df[columns]

    if dataset == "ML-children":
        columns = columns_ml
        df = df[columns]

    plot_prominence(df, metric)
    plot_metric_ttest(df, metric)
