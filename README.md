# Exploring the Effect of Recommendation Algorithms on Exposing Children to Stereotypes

This repository contains the code to reproduce the empirical exploration accomplished in the paper:
**Mirror, Mirror: Exploring Stereotype Presence among Top-N Recommendations**, submitted to the TORS special issue for Recommender systems for good.





## Requirements

In order to reproduce the steps of the empirical exploration, the following tools and datasets are required.

- [Elliot](https://github.com/sisinflab/elliot)
- [Movielens-1M](https://grouplens.org/datasets/movielens/1m/) dataset
- [Goodreads](https://mengtingwan.github.io/data/goodreads.html#datasets) with "children" Genre
 (`goodreads_books_children.json.gz`)

## 1. Dataset Preprocessing
Create the trainingsets for MovieLens (ML) and Goodreads (GR).

- For GR, create a function that filters for items annotated with the "Children" Genre.

For both datasets, the remaining preprocessing steps are handled by the `config_file`s.

## 2. Run Elliot
- Generate the recommendations with Elliot (`.tsv` files, see [docs](https://elliot.readthedocs.io/en/latest/guide/introduction.html)). 
- See requirements_elliot.txt for the requirements and the files in the directory `config_file`s for the detailed configurations for Elliot. 

## 3. Create Evaluation Subset
- For ML, filter the results of Elliot by users with age < 18 (ML-children)


## 4. Predict stereotypes using the SDMs
- Generate files that indicate whether a stereotype was found for each item in the recommendation list. For examples, see `Results/SDM`.
- Create stereotype predictions for all items using each SDM for each sterotype (NGIM only Gender)

### Preparation
- Gather the item descriptions, which are included in the Goodreads dataset. For Movielens extract the item description from the [Movie-Database](https://www.themoviedb.org/)
- Save the item descriptions as csv files with the column names: "id", "description" as
1. Gender Stereotype Detection `Methods/data/ml_descriptions_processed.csv`
2. Gender Stereotype Detection `Methods/data/gr_descriptions_processed.csv`

### NGIM
Prepare the item descriptions of books and movie Titles and compute and save the predicted scores by running the script: `Gender Stereotype Detection Methods/NGIM/ngim.py`

### BiasMeter
- Apply [BiasMeter](https://github.com/YacineGACI/BiasMeter) to the Book and Item Description. 
- If BiasMeter predicts a value > 0.7, classify the item as stereotypical
- Save the predicted scores for each 'stereotype' as `Gender Stereotype Detection Methods/results/{dataset}_biasmeter_{stereotype}.csv`

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

## 5. Performance Evaluation
- Evaluate the performance using results by Elliot. Consider that the performance for ML needs to be evaluated only for users whose age < 18

## 6. Stereotype Evaluation
- Place all recommendations for each dataset in a separate folder (see directory `input_recommendations`).
- Run `calculate_stereotype_metrics.py` and make sure the path to the recommendations are correct (**lines 244 & 245**).
- All the metrics for each RA will be stored as *.csv* files in "Results/SDM/..."
- Run `plot_metrics.py` after the results are stored to plot the metrics.

- Remark that we re-run the statistics with `R`. Those scripts can be found in `Additional_Statistical_Eval`





