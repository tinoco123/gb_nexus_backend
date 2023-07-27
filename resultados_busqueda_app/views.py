from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def search_results(request):
    return render(request, "search_results.html")
