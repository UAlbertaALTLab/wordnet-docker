import re
from . import nltk

diff_regexp = re.compile(r"\s*<<<<<<< (?P<left_branch>.*)\n(?P<left_lines>(.*\n)*)\s*=======\s*\n(?P<right_lines>(.*\n)*)\s*>>>>>>> (?P<right_branch>.*)\n")
wiktionary_regexp = re.compile(r"^(?P<entry>.*)\s+(?P<kind>\S*)\.\s+#w")
toolbox_regexp = re.compile(r"^(?P<entry>.*)\s+(?P<kind>\S*)\.\s+#")

def parse(text):
    entries = diff_regexp.match(text)
    if not entries:
        return None
    return {
        "left_branch": entries["left_branch"].strip(),
        "left_lines": [line.strip() for line in entries["left_lines"].splitlines()],
        "right_branch": entries["right_branch"].strip(),
        "right_lines": [line.strip() for line in entries["right_lines"].splitlines()]
    }

def resolve(entry: str):
    if not entry.startswith("\\gl"):
        return { "is_field" : False, "text": entry }
    _, _, text = entry.partition(" ")

    wiktionary = wiktionary_regexp.match(text)
    if wiktionary:
        wiki_entry = wiktionary["entry"]
        return { "is_field" : True, "text": entry.strip(), "wiktionary_entry":  wiktionary["entry"], "wiktionary_kind": wiktionary["kind"], "wiktionary_url": f"https://en.wiktionary.org/wiki/{wiki_entry}#English", "is_wiktionary": True}
    
    toolbox = toolbox_regexp.match(text)
    if toolbox:
        return { "is_field" : True, "text": entry.strip(), "results" : nltk.search(toolbox["entry"]), "is_toolbox": True}
    
    return { "is_field": True, "text": entry.strip(), "results": nltk.search(text)}
    
    
    