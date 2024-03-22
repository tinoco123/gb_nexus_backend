from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def sign_in(request):
    if request.user.is_authenticated:
        return redirect("keywords")
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
                    if user.terms_accepted == False:
                        return redirect("terms_conditions")
                    else:
                        return redirect("keywords")
                else:
                    messages.error(request, "Cuenta inactiva o datos incorrectos")
                    return render(request, "login.html", {"form": login_form})
            else:
                return render(request, "login.html", {"form": login_form})


@login_required
def sign_out(request):
    logout(request)
    return redirect("sign_in")


def get_terms_conditions(request):
    if request.method == "GET":
        return render(request, "terms_conditions.html")
    elif request.method == "POST":
        terms_accepted = request.POST.get("accept_terms")
        if terms_accepted:
            user = request.user
            if user is not None:
                user.terms_accepted = True
                user.save()
                return redirect("keywords")
        else:
            return redirect("terms_conditions")
