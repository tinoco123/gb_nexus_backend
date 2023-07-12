from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import CreateUserForm
from tipos_usuarios.models import Usuario
from datetime import date, datetime
import json


@login_required
def users(request):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()
    else:
        if request.method == "GET":
            create_user_form = CreateUserForm()
            users = list(Usuario.objects.values(
                "id", "first_name", "last_name", "company", "date_joined"))
            usuarios_json = json.dumps(users, default=date_serializer)
            return render(request, 'usuarios.html', {"users": usuarios_json,
                                                     "create_user_form": create_user_form})


@login_required
def create_user(request):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            create_user_form = CreateUserForm(request.POST)
            if create_user_form.is_valid():
                email = create_user_form.cleaned_data["email"]
                password = create_user_form.cleaned_data["password"]
                name = create_user_form.cleaned_data["first_name"]
                date_birth = create_user_form.cleaned_data["date_birth"]
                Usuario.objects.create_user(
                    email=email, password=password,first_name=name, date_birth=date_birth)
                return redirect("users")


def date_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
