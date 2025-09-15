from django.shortcuts import render
from itertools import zip_longest

from . import nltk
from . import diff

def index(request):
    search = request.GET.get("search", "")   if request.method == "GET" else ""

    context = {
        "wordnet": "We want to see the wizard of oz!",
        "search": search,
        "results": nltk.search(search)
    }
    return render(request, "wordnet/index.html", context)

def diff_view(request):
    text = request.POST.get("text", "") if request.method == "POST" else ""
    parsed = diff.parse(text)
    if not parsed:
        return render(request, "wordnet/diff.html", {})
    
    left_results = [diff.resolve(entry) for entry in parsed["left_lines"]]
    right_results = [diff.resolve(entry) for entry in parsed["right_lines"]]

    
    context = {
        "text": text,
        "left_branch": parsed["left_branch"],
        "right_branch": parsed["right_branch"],
        "results": [ (diff.resolve(entry1) if entry1 else {"is_emtpy": True},
                      diff.resolve(entry2) if entry2 else {"is_empty": True})
                      for entry1, entry2 in zip_longest(parsed["left_lines"], parsed["right_lines"])]
    }
    return render(request, "wordnet/diff.html", context)