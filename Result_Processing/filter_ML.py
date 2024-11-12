import pandas as pd
import os
import glob


rec_models_path = '../input_recommendations/movielens/*.tsv'

files = glob.glob(rec_models_path)

recommendations_ml = pd.read_csv("../data/recommendations_ml.tsv")

users_ml = pd.read_csv("../data/ml-1m/users.csv")

users_ml = users_ml[users_ml['Age'] == 1]

for file in files:
    recommendations = pd.read_csv(file)
    recommendations = recommendations[recommendations['user_id'].isin(users_ml['user_id'])]
    recommendations.to_csv(file.replace('movielens', 'movielens_child'), index=False)

