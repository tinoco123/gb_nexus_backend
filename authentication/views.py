from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('keywords')
    else:
        if request.method == "GET":
            login_form = LoginForm()
            return render(request, "login.html", {"form": login_form})

        if request.method == "POST":
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                email = login_form.cleaned_data["email"]
                password = login_form.cleaned_data["password"]

                user = authenticate(request, email=email, password=password)

                if user is not None:
                    login(request, user)
                    return redirect('keywords')
                else:
                    messages.error(request, "Cuenta inactiva o datos incorrectos")
                    return render(request, "login.html", {"form": login_form})
            else:
                return render(request, "login.html", {"form": login_form})


@login_required
def sign_out(request):
    logout(request)
    return redirect('sign_in')
