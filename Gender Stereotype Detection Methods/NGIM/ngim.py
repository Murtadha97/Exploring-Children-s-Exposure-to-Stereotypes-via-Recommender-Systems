import sys

import pandas as pd
import ast
from Genesis import write_model_labels
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import imdb
from flair.data import Sentence
from flair.models import SequenceTagger

def label_cast(cast):
     if cast == []:
         return "Female"

     predictions = pipeline.predict(cast)
     result = [label['label'] for label in predictions]

     count_male_labels = result.count("Male")
     count_female_labels = result.count("Female")

     if count_male_labels >= count_female_labels:
         return "Male"
     else:
         return "Female"

import argparse
if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='Run NGIM stereotype detection model')
    # parser.add_argument('--dataset', type=str, help='The dataset to analyse. Either ml or gr', required=True)

    # args = parser.parse_args()
    # dataset = args.dataset
    dataset = "gr" 
    if dataset == "ml":
        items_to_label = pd.read_csv('../data/ml-1m/movies.dat', sep='::', engine='python')
        ia = imdb.IMDb()
        items_to_label['Cast'] = None
        for i, movie in items_to_label.iterrows():
            
            

            results = ia.search_movie(movie['Title'])

            movie = results[0]

            ia.update(movie)

            cast = movie['cast'][:5]
            if cast is None:
                cast_names = []
            else:
                cast_names = [person['name'] for person in cast]
        
            # Update the 'Cast' column in the DataFrame
            items_to_label.at[i, 'Cast'] = cast_names

    if dataset == "gr":
        items_to_label = pd.read_csv('../data/goodreads/books.csv')
        
        items_to_label['Cast'] = None
        tagger = SequenceTagger.load('ner')
        for i, book in items_to_label.iterrows():
            book_description = book['description']
            
            if book_description:
                # Create a Sentence object
                sentence = Sentence(book_description)
                
                # Predict entities in the sentence
                tagger.predict(sentence)
                
                # Filter for entities labeled as 'PER' (Person)
                cast_names = [entity.text for entity in sentence.get_spans('ner') if entity.get_label().value == 'PER']
            else:
                cast_names = []
            
            # Update the 'Cast' column in the DataFrame
            items_to_label.at[i, 'Cast'] = cast_names

    
    tokenizer = AutoTokenizer.from_pretrained("malcolm/REA_GenderIdentification_v1")

    model = AutoModelForSequenceClassification.from_pretrained("malcolm/REA_GenderIdentification_v1", id2label={0: 'Female', 1: 'Male'})

    pipeline = TextClassificationPipeline(model=model, tokenizer=tokenizer, framework='pt', device=0)

    items_to_label['Label'] = items_to_label['Cast'].apply(label_cast)


    items_to_label['Label'] = items_to_label['Label'].apply(lambda x: 1 if x == "Male" else 0)
    
    if dataset == "gr":
        labeled_data = items_to_label[['id', 'Label']]
    elif dataset == "ml":
        labeled_data = items_to_label[['MovieID', 'Label']]
        
    labeled_data.columns = ['ItemID', 'Label']
    
    if dataset == "ml":
        labeled_data.to_csv("movielens-1m_ngim_gender.csv", index=False)
    elif dataset == "gr":
        labeled_data.to_csv("goodreads_ngim_gender.csv", index=False)
