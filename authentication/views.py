from django.shortcuts import render

def sign_in(request):
    if request.method == "GET":
        return render(request, "login.html")
