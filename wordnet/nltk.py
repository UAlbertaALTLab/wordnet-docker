from nltk.corpus import wordnet as wn

def candidates(keyword):
    if not keyword:
        return []
    result = wn.synsets(keyword)
    if len(result) == 0 :
        result = [wn.synset(keyword)]
    return result

def name_format(name):
    return name

def normalize_result(result):
    return {
        "name" : name_format(result.name),
        "pos"  : result.pos,
        "definition" : result.definition,
        "lemmas" : [name_format(lemma.name) for lemma in result.lemmas()],
        "hyponyms" : [name_format(r.name) for r in result.hyponyms()],
        "hypernyms" : [name_format(r.name) for r in result.hypernyms()]
    }

def search(keyword):
    return [normalize_result(result) for result in candidates(keyword)]
