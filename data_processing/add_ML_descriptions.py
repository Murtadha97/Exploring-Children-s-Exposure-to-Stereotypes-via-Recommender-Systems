import sys

import pandas as pd

if __name__ == '__main__':
    movies_ml = pd.read_csv('Datasets/ml-1m/movies.dat', sep='::', names=['MovieID', 'original_title', 'Genres'])
    movies_metadata = pd.read_csv('Datasets/ml-1m/movies_metadata.csv', sep=',')


    metadata_to_merge = movies_metadata[['adult', 'title', 'overview']].copy()


    movies_ml[['Year']] = movies_ml.title.str.extract(r'(\(\d+\))', expand=True)
    movies_ml[['title']] = movies_ml.title.str.replace(r'\s*\(\d+\)\s*', '', n=1)

    merged_movies = pd.merge(movies_ml, metadata_to_merge, on='title', how='left')
    merged_movies = merged_movies.drop_duplicates(keep="first", subset=["title", "Year"]).reset_index(drop=True)

    merged_movies = merged_movies[['MovieID', 'title', 'Year', 'Cast', 'Genres', 'overview', 'adult']]

    merged_movies.rename(columns={'overview': 'description'}, inplace=True)

    merged_movies.to_csv('movielens-1m_descriptions.csv', sep=',', index=False)

    