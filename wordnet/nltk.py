from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
import re

format_regexp = r'^\s*\((?P<pos>\w+)\)\s+(?P<stem>[^\s]+)\s*\#\s*(?P<num>\d+)\s*\Z'

def candidates(keyword):
    if not keyword:
        return []
    real_keyword = normalize_keyword(keyword)
    result = wn.synsets(real_keyword)
    if len(result) == 0 :
        try:
            result = [wn.synset(real_keyword)]
        except ValueError:
            result = []
    return result

def name_format(synset : Synset):
    data = synset.name().split(".")
    entry = ".".join(data[0:-2])
    return f"({data[-2]}) {entry}#{int(data[-1])}"

def normalize_keyword(keyword: str) -> str:
    matches = re.match(format_regexp, keyword)
    if matches:
        return matches['stem']+'.'+matches['pos']+'.'+matches['num']
    return keyword

def normalize_result(result):
    return {
        "name" : name_format(result),
        "pos"  : result.pos,
        "definition" : result.definition,
        "lemmas" : [lemma.name for lemma in result.lemmas()],
        "hyponyms" : [name_format(r) for r in result.hyponyms()],
        "hypernyms" : [name_format(r) for r in result.hypernyms()],
        "holonyms" : [name_format(r) for r in result.member_holonyms()]
    }

def search(keyword):
    return [normalize_result(result) for result in candidates(keyword)]
