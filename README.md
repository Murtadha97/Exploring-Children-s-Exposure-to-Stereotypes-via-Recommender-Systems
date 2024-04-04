# Exploring the Effect of Recommendation Algorithms on Exposing Children to Stereotypes

This repository contains the necessary data to reproduce the empirical evaluation accomplished in the paper:
**Exploring the Effect of Recommendation Algorithms on Exposing Children to Stereotypes**, submitted to RecSys '24



## Abstract

Children form stereotypes by observing stereotypical expressions in media during childhood, influencing future beliefs, attitudes, and behavior. Stereotypical information, often negative in nature, can occur in all kinds of media that children are exposed to during their frequent interactions with online platforms such as streaming services and social media platforms. Items on those platforms are commonly selected by recommendation algorithms (\RAs{}), which may inadvertently expose children to stereotypical content. Given children's vulnerability, we need to understand the potential negative impact recommended items can have on children. However, the extent to which \RAs{} expose children to stereotypes, and consequently the potential harm they may cause, remains uncertain.


To address this knowledge gap, we conduct an empirical evaluation that explores the degree to which \texttt{RAs} present children to stereotypes. Our study focuses on evaluating the presence of Gender, Race, and Religion stereotypes in the top-$10$ recommendations made to children across two prominent item categories: Movies and Books. We find that Gender stereotypes are the most common, appearing in almost every recommendation list. Moreover, our results suggest that the majority of RAs{} exhibit a systematic tendency to amplify stereotypes in the recommendations, underscoring the potential risks that recommendation algorithms pose to children in perpetuating and reinforcing harmful stereotypes.



## Requirements

In order to reproduce the steps of the empirical exploration, the following tools and datasets are required.

- [Elliot](https://github.com/sisinflab/elliot)
- [Movielens-1M](https://grouplens.org/datasets/movielens/1m/) dataset
- [Goodreads](https://mengtingwan.github.io/data/goodreads.html#datasets) Children Genre


## 1. Dataset Preprocessing
Create the trainingsets for MovieLens (ML) and Goodreads (GR).


- For GR, create a function that filters for items annotated with the "Children" Genre.

For both datasets, the remaining preprocessing steps can be found in the **config_files**.

## 2. Run Elliot
- Generate the recommendations with Elliot (**.tsv* files, see [docs](https://elliot.readthedocs.io/en/latest/guide/introduction.html)). 
- See requirements_elliot.txt for the requirements and the files in the directory **config_files** for the detailed configurations for Elliot. 

## 3. Create Evaluation Subset
- For ML, filter the results of Elliot by users with age < 18 (ML-children)


## 4. Predict stereotypes using the SDMs
- Generate files that indicate whether a stereotype was found for each item in the recommendation list. For examples, see **Results/SDM**.
- Create stereotype predictions for all items using each SDM for each sterotype (NGIM only Gender)

### NGIM
- For ML, query the movie title and search for it using Python's [IMDb-library](https://pypi.org/project/IMDbPY/) and extract the top 5 cast members from the first result.
- For GR, extract the characters from the book descriptions using Flair's [Named-Entity-Recognition](https://pypi.org/project/flair/) tool.
- For both datasets, predict the genders of the characters/cast members using the [Gender-Guesser-library](https://pypi.org/project/gender-guesser/).
- For each item, tag the item **1** if the number of male characters is higher than the number of female characters.
- If no characters could be retrieved or the number of male characters is not higher, tag the item with **0**

### BiasMeter
- For ML, extract the item description from the [Movie-Database](https://www.themoviedb.org/)
- Apply [BiasMeter](https://hal.science/hal-03626753/) to the Book and Item Description
- If BiasMeter predicts a value > 0.7, classify the item as stereotypical

### ChatGPT
- For ML, extract the item description from the [Movie-Database](https://www.themoviedb.org/)
- Get access to chat-gpt using OpenAI's [API](https://github.com/openai/openai-cookbook/blob/main/examples/api_request_parallel_processor.py); we used the model gpt-3.5-turbo-0613
- Request a response using the input prompt mentioned in the paper in combination with the item description
- Predict a stereotype if GPT's stereotype probability is > 0.7


## 5. Performance Evaluation
- Evaluate the performance metrics using Elliot with a 5 fold 80-20 train-test split. Note that the testset for ML should only consist of users with age < 18

## 6. Stereotype Evaluation
- Place all recommendations for each dataset in a separate folder (see folder **input_recommendations**).
- Run `calculate_stereotype_metrics.py` and make sure the path to the recommendations are correct (**lines 244 & 245**).
- All the metrics for each RA will be stored as *.csv* files in "Results/SDM/..."
- Run `plot_metrics.py` after the results are stored to plot the metrics.



**The full results of our evaluation can be seen in the directory "Results"**





