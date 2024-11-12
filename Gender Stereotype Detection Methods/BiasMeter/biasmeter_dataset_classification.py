import math
import sys
from ast import literal_eval
import pandas as pd
from nltk.tokenize import sent_tokenize

from bias_meter import compute_sentence_stereotype, enablePrint, blockPrint

enablePrint()


def classify_sentence(sentences):
    enablePrint()
    results = []
    value = sentences
    print(value)
    print(type(value))

    try:
        # value = literal_eval(sentences)
        if type(value) == list:
            for s in value:
                result = compute_sentence_stereotype(s, normalization_function=lambda x: math.log(x + 1))
                results.append(result)
        else:
            return compute_sentence_stereotype("", normalization_function=lambda x: math.log(x + 1))
    except Exception as e:
        print(f"An exception occurred: {e} for sentence {sentences}")
        return None
    print(results)

    return results


if __name__ == '__main__':
    # Movielens classification
    movielens = pd.read_csv("data/movielens_biasmeter_tokenized.csv", encoding="utf-8")
    movielens['sent_tokenize'] = movielens['sent_tokenize'].fillna("")
    
    movielens['biasmeter_results'] = movielens['sent_tokenize'].apply(lambda x: classify_sentence(x))
    
    movielens.to_csv("movielens_biasmeter_labeled_paper-evaluation-metric.csv", index=False)


    goodreads = pd.read_csv("../../Experiments/Results/biasmeter/goodreads/goodreads_biasmeter_tokenized.csv",
                            encoding="utf-8")

    goodreads['sent_tokenize'] = goodreads['sent_tokenize'].fillna("")

    goodreads['biasmeter_results'] = goodreads['sent_tokenize'].apply(classify_sentence)

    goodreads.to_csv("goodreads_biasmeter_labeled_paper-evaluation-metric.csv", index=False)
