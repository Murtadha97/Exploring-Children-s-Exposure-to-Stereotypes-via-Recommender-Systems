import pandas as pd
import os
import argparse

parser = argparse.ArgumentParser(description='Tokenize the biasmeter datasets.')
parser.add_argument('--dataset', type=str, help='Dataset to tokenize', choices=['ml', 'gr'], required=True)
args = parser.parse_args()

dataset = args.dataset

dataset_dir = '../data'

if dataset == 'ml':
    st_data_path = dataset_dir + '/raw/Stereotypes/MovieLens_Descriptions.csv'
    save_data_path = "../../data/ml_descriptions_processed.csv"
    st_data = pd.read_csv(st_data_path)

    st_data = st_data.rename(columns={'MovieID': 'id', 'description': 'description'})
    
    
if dataset == 'gr':
    st_data_path = dataset_dir + '/goodreads_descriptions.csv'
    save_data_path = "../data/gr_descriptions_processed.csv"
    st_data = pd.read_csv(st_data_path)

    
    st_data = st_data.rename(columns={'book_id': 'id', 'description': 'description'})

    
st_data.to_csv(save_data_path, index=False, columns=['id', 'description'])

