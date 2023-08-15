from django.http import HttpResponse
from django.shortcuts import render


def clients(request):
    return HttpResponse("Clientes")
