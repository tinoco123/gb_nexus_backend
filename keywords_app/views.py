from django.shortcuts import render
from .forms import KeywordForm

def keywords(request):
    keyword_form = KeywordForm()
    return render(request, 'keywords.html', {"create_keyword_form": keyword_form})
