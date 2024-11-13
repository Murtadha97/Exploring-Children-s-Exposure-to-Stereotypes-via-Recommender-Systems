import pandas as pd
from nltk.tokenize import sent_tokenize
import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tokenize the biasmeter datasets.')
    parser.add_argument('--dataset', type=str, help='Dataset to tokenize', choices=['goodreads', 'movielens'], required=True)
    
    dataset = parser.parse_args().dataset
    
    if dataset == 'goodreads':
        goodreads = pd.read_csv("../../data/gr_descriptions_processed.csv")
        goodreads['description'] = goodreads['description'].fillna('')
        goodreads['sent_tokenize'] = goodreads['description'].apply(lambda x: sent_tokenize(x) if x != "" else x)
        goodreads.to_csv("data/goodreads_biasmeter_tokenized.csv", index=False)
        
    elif dataset == 'movielens':
        movielens = pd.read_csv("../../data/gr_descriptions_processed.csv")
        movielens['description'] = movielens['description'].fillna('')
        movielens['sent_tokenize'] = movielens['description'].apply(lambda x: sent_tokenize(x) if x != "" else x)
        movielens.to_csv("data/movielens_biasmeter_tokenized.csv", index=False)
        
    else:
        raise ValueError("Invalid dataset name.")
