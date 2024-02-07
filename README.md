# Exploring Children's Exposure to Stereotypes via Recommender Systems

This repository contains the files used during my thesis research. 



## Abstract

"Girls are bad at math, but are better than boys in linguistic subjects!" Such stereotypes, potentially manifesting through various sources, can impact children's development and negatively affect their academic performance. In this work, we study the presence of stereotypes among the Top-10 suggestions of Recommender Algorithms. In particular, we conduct an empirical exploration using an extensive suite of Recommender Algorithms on two well-known datasets from different domains: MovieLens-1M (movies) and Goodreads (books). We aim to assess the presence of gender, race, and religion stereotypes. We utilize three stereotype detection models, based on machine learning and Large Language models, and we leverage performance metrics to contextualize the Recommender Algorithms and stereotype prominence metrics to measure the extent of their presence in the recommendations. Outcomes from this work evidence that stereotypes are not equally prominent across all Recommender Algorithms, with certain content-based and deep-learning models showing higher tendencies to recommend stereotypical content to children. Findings emerging from our exploration result in several implications for researchers and practitioners to consider when designing and deploying Recommender Algorithms, especially when children are also interacting with these systems. Furthermore, this work presents a blueprint in which stereotype detection can be expanded to other domains, other types of stereotypes, and other demographic user groups.



## Requirements

In order to reproduce our steps you need the following:

- [Elliot](https://github.com/sisinflab/elliot)
- [Movielens-1M](https://grouplens.org/datasets/movielens/1m/) dataset
- [Goodreads](https://mengtingwan.github.io/data/goodreads.html#datasets) Children Genre



## How to run

1. Generate the recommendations with Elliot (**.tsv* files, see [docs](https://elliot.readthedocs.io/en/latest/guide/introduction.html)). 
2. Place all recommendations for each dataset in a separate folder (see folder **input_recommendations**).
3. Run `calculate_stereotype_metrics.py` and make sure the path to the recommendations are correct (**lines 244 & 245**).
4. All the metrics for each RA will be stored as *.csv* files in "Results/SDM/..."
5. Run `plot_metrics.py` after the results are stored to plot the metrics.







