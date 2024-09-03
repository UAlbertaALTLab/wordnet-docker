from django.shortcuts import render
from . import nltk

def index(request):
    search = request.GET.get("search", "")   if request.method == "GET" else ""

    context = {
        "wordnet": "We want to see the wizard of oz!",
        "search": search,
        "results": results(search)
    }
    return render(request, "wordnet/index.html", context)

def results(search):
    return nltk.search(search) if search else []