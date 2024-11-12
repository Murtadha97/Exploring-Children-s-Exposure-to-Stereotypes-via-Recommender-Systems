import sys

import pandas as pd
import gzip
import json


# from googletrans import Translator, constants


def load_data(file_name, head=500):
    """"
    This function loads the goodreads files. It comes from the official goodreads notebook file.
    """
    # count = 0
    data = []
    with gzip.open(file_name) as fin:
        for l in fin:
            d = json.loads(l)
            # count += 1
            data.append(d)

            # break if reaches the 100th line
            # if (head is not None) and (count > head):
            #     break
    return data




if __name__ == '__main__':


    df_books = pd.read_json("goodreads_books_children.json.gz", lines=True)
    df_books = df_books.set_index('book_id')


    df_interactions = pd.read_json("goodreads_interactions_children.json.gz", lines=True)


    cols = ["user_id", "book_id", "review_id", "is_read", "rating"]
    df = df_interactions[cols]
    df_rated = df.loc[df.is_read]

    df_rated.to_csv("goodreads_ratings.tsv", sep="\t", columns=["user_id", "book_id", "rating"], index=False, header=False)

    df_books.fillna("")

    df_books.to_csv("goodreads_descriptions.csv", index=False, columns=["book_id", "url", "image_url", "language_code", "description"])