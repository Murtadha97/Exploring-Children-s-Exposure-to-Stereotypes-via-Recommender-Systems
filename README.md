# Exploring the Effect of Recommendation Algorithms on Exposing Children to Stereotypes

This repository contains the code to reproduce the empirical exploration accomplished in the paper:
**Mirror, Mirror: Exploring Stereotype Presence Among Top-N Recommendations Than May Reach Children**, submitted to the TORS special issue on Recommender Systems for Good.





## Requirements

In order to reproduce the steps of the empirical exploration, the following tools and datasets are required.

- [Elliot](https://github.com/sisinflab/elliot)
- [Movielens-1M](https://grouplens.org/datasets/movielens/1m/) dataset
- [Goodreads](https://mengtingwan.github.io/data/goodreads.html#datasets) with "children" Genre
 (`goodreads_interactions_children.json.gz`)
 - [TMDB 10000 Popular Movies](https://www.kaggle.com/datasets/muqarrishzaib/tmdb-10000-movies-dataset)
 - Add the datasets to the `data` directory


## 1. Dataset Preprocessing

- run `preprocess_data/read_goodreads.py`
- run `preprocess_data/add_ML_descriptions.py`


For both datasets, the remaining preprocessing steps are handled by the `config_file`s and Elliot.



## 2. Run Elliot
- Install Elliot in the main directory
- Create conda environment
```
conda create --yes --name elliot-env python=3.8
conda activate elliot-env
cd Experiment_2 
git clone https://github.com//sisinflab/elliot.git && cd elliot
pip install --upgrade pip
pip install -e . --verbose
```

- Add the rating data to elliot: `elliot/data/goodreads_ratings.tsv`. Movielens data should automatically be added by installing Elliot
- Generate the recommendations with Elliot (`.tsv` files, see [docs](https://elliot.readthedocs.io/en/latest/guide/introduction.html)). 
- See requirements_elliot.txt for the requirements and the files in the directory `config_file`s for the detailed configurations for Elliot. 

## 3. Create Evaluation Subset
- Add recommendation directories to the directory `input_recommendations` as `input_recommendations/goodreads/*.tsv` and  `input_recommendations/movielens/*.tsv`
- For ML, filter the results of Elliot by users with age < 18 (ML-children) by running `Result_Processing/filter_ML.py`


## 4. Predict stereotypes using the SDMs
- Generate files that indicate whether a stereotype was found for each item in the recommendation list.
- Create stereotype predictions for all items using each SDM for each sterotype (NGIM only Gender)

### Preparation
- By using the `data_processing/create_subset.py` script save the item descriptions as csv files with the column names: "id", "description" as
1. Gender Stereotype Detection `data/ml_descriptions_processed.csv`
2. Gender Stereotype Detection `data/gr_descriptions_processed.csv`

### NGIM
Prepare the item descriptions of books and movie Titles and compute and save the predicted scores by running the script: `Gender Stereotype Detection Methods/NGIM/ngim.py`

### BiasMeter
- Get [BiasMeter](https://github.com/YacineGACI/BiasMeter) and fit the models. Add all scripts and data to `Gender Stereotype Detection methods/BiasMeter` 
- Tokenize MovieLens and Goodreads with `Gender Stereotype Detection Methods/BiasMeter/tokenize_biasmeter.py`
- Run `Gender Stereotype Detection Methods/BiasMeter/biasmeter_dataset_classification.py` in order to analyze the individual sentences in the descriptions.
- Run `Gender Stereotype Detection Methods/BiasMeter/calc_cf.py` in order to compute the Stanford Certainty Factor and save the predicted labels.


### ChatGPT
- Get access to chat-gpt using OpenAI's [API parallel processor](https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py); we used the model gpt-3.5-turbo
- Generate input prompts using `Gender Stereotype Detection Methods/GPT/chatgpt_label_datasets.py`
- Run the input prompts using the abovementioned parallel processor; Example calls:
    ```
    python "api_request_parallel_processor.py" --requests_filepath "Gender Stereotype Detection Methods/data/jobs_gr_1.jsonl" --save_filepath "Gender Stereotype Detection Methods/results/sdm_results_gr.jsonl" --api_key **your_api_key** --request_url "https://api.openai.com/v1/chat/completions" --max_requests_per_minute 400 --max_tokens_per_minute 100000
    ```
    ```
    python "api_request_parallel_processor.py" --requests_filepath "Gender Stereotype Detection Methods/data/jobs_gr_2.jsonl" --save_filepath "Gender Stereotype Detection Methods/results/sdm_results_gr.jsonl" --api_key **your_api_key** --request_url "https://api.openai.com/v1/chat/completions" --max_requests_per_minute 400 --max_tokens_per_minute 100000
    ```
    ```
    python "api_request_parallel_processor.py" --requests_filepath "Gender Stereotype Detection Methods/data/jobs_ml.jsonl" --save_filepath "Gender Stereotype Detection Methods/results/sdm_results_gr.jsonl" --api_key **your_api_key** --request_url "https://api.openai.com/v1/chat/completions" --max_requests_per_minute 400 --max_tokens_per_minute 100000
    ```
- Predict a stereotype if GPT's stereotype probability is > 0.7 by running the script `Gender Stereotype Detection Methods/GPT/chatgpt_read_results.py`

### Processing Results
- Run `Gender Stereotype Detection Methods/Genesis.py` in order to summarize the results from the different metrics.


## 5. Stereotype Evaluation
- Run `calculate_stereotype_metrics.py` and make sure the path to the recommendations are correct (**lines 244 & 245**).
- All the metrics for each RA will be stored as *.csv* files in "Results/SDM/..."
- Run `plot_metrics.py` after the results are stored to plot the metrics.

- Remark that we re-run the statistics with `R`. Those scripts can be found in `Additional_Statistical_Eval`





