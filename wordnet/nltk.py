from nltk.corpus import wordnet as wn

def search(keyword):
    result = wn.synsets(keyword)
    if len(result) == 0 :
        result = [wn.synset(keyword)]
    return result