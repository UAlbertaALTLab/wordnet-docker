from nltk.corpus import wordnet as wn
from nltk.corpus.reader.wordnet import Synset
from itertools import groupby
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

def name_format(synset : Synset, new_index = None, new_key = None):
    if new_index is None or new_key is None:
        data = synset.name().split(".")
        entry = ".".join(data[0:-2])
        return f"({data[-2]}) {entry}#{int(data[-1])}"
    candidate = '_'.join(new_key.split())
    if candidate in [lemma.name() for lemma in synset.lemmas()]:
        return f"({synset.pos()}) {candidate}#{int(new_index+1)}"
    candidate = wn.morphy(('_'.join(new_key.split())))
    if candidate in [lemma.name() for lemma in synset.lemmas()]:
        return f"({synset.pos()}) {candidate}#{int(new_index+1)}"
    data = synset.name().split(".")
    entry = ".".join(data[0:-2])
    return f"({data[-2]}) {entry}#{int(data[-1])}"

wordnet_keys = dict(v='v.', n='n.', a='a.', r='adv.', s='a.')

def name_format_toolbox(synset : Synset, new_index, new_key):
    pos = wordnet_keys[synset.pos()]
    if new_index is None or new_key is None:
        data = synset.name().split(".")
        entry = " ".join(".".join(data[0:-2]).split("_"))
        return f"{entry} {pos} #{int(data[-1])}"
    candidate = '_'.join(new_key.split())
    if candidate in [lemma.name() for lemma in synset.lemmas()]:
        return f"{' '.join(candidate.split('_'))} {pos} #{int(new_index+1)}"
    candidate = wn.morphy('_'.join(new_key.split()))
    if candidate in [lemma.name() for lemma in synset.lemmas()]:
        return f"{' '.join(candidate.split('_'))} {pos} #{int(new_index+1)}"
    data = synset.name().split(".")
    entry = " ".join(".".join(data[0:-2]).split("_"))
    return f"{entry} {pos} #{int(data[-1])}"

    
def normalize_keyword(keyword: str) -> str:
    matches = re.match(format_regexp, keyword)
    if matches:
        return matches['stem']+'.'+matches['pos']+'.'+matches['num']
    return '_'.join(keyword.split())

def is_exact_search(keyword:str) -> bool:
    return re.match(format_regexp, keyword)

def reverse_normalized_keyword(keyword: str) -> str:
    matches = re.match(format_regexp, keyword)
    if matches:
        return ' '.join(matches['stem'].split('_'))
    return ' '.join(keyword.split('_'))


def normalize_result(result, new_index = None, new_key = None):
    return {
        "name" : name_format(result, new_index, new_key),
        "toolbox_name" : name_format_toolbox(result, new_index, new_key), 
        "pos"  : result.pos,
        "definition" : result.definition,
        "lemmas" : [lemma.name for lemma in result.lemmas()],
        "hyponyms" : [name_format(r) for r in result.hyponyms()],
        "hypernyms" : [name_format(r) for r in result.hypernyms()],
        "holonyms" : [name_format(r) for r in result.member_holonyms()]
    }

def search(keyword):
    entry = reverse_normalized_keyword(keyword)
    results = groupby(candidates(keyword), key = lambda x : x.name().split('.')[-2])
    if is_exact_search(keyword):
        print(keyword)
        return enumerate([normalize_result(result) for _, grouped in results for result in grouped])
    answers = [normalize_result(result, index, entry) for _, grouped in results for index, result in enumerate(grouped)]
    return enumerate(answers)
