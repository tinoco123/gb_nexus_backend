from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseNotAllowed
from .forms import UserForm, EditUserForm
from tipos_usuarios.models import Usuario
from datetime import date, datetime
import json


@login_required
def users(request):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()
    else:
        if request.method == "GET":
            user_form = UserForm()
            users = list(Usuario.objects.values(
                "id", "first_name", "last_name", "company", "date_joined"))
            usuarios_json = json.dumps(users, default=date_serializer)
            return render(request, 'usuarios.html', {"users": usuarios_json,
                                                     "user_form": user_form})
        else:
            return HttpResponseNotAllowed("Método No Permitido")


@login_required
def create_user(request):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()
    else:
        if request.method == "POST":
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                email = user_form.cleaned_data["email"]
                password = user_form.cleaned_data["password"]
                first_name = user_form.cleaned_data["first_name"]
                last_name = user_form.cleaned_data["last_name"]
                address = user_form.cleaned_data["address"]
                company = user_form.cleaned_data["company"]
                date_birth = user_form.cleaned_data["date_birth"]
                Usuario.objects.create(email=email, password=password, first_name=first_name,
                                       last_name=last_name, address=address, company=company, date_birth=date_birth)
                return redirect("users")
            else:
                errors = user_form.errors.as_json(escape_html=True)
                return JsonResponse({'success': False, 'errors': errors}, status=400)
        else:
            return HttpResponseNotAllowed(permitted_methods=("POST"))


@login_required
def edit_user(request, user_id):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()

    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        user = get_object_or_404(Usuario, id=user_id)

        user_form = EditUserForm(request.POST, instance=user)
        if user_form.is_valid():
            email = user_form.cleaned_data["email"]
            password = user_form.cleaned_data["password"]
            first_name = user_form.cleaned_data["first_name"]
            last_name = user_form.cleaned_data["last_name"]
            address = user_form.cleaned_data["address"]
            company = user_form.cleaned_data["company"]
            date_birth = user_form.cleaned_data["date_birth"]
            Usuario.objects.edit(id=user_id, email=email, password=password, first_name=first_name,
                                   last_name=last_name, address=address, company=company, date_birth=date_birth)
            return redirect("users")
        else:
            errors = user_form.errors.as_json(escape_html=True)
            print(errors)
            return JsonResponse({'success': False, 'errors': errors}, status=400)


@login_required
def get_user(request, user_id):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()

    if request.method == "GET":
        user = get_object_or_404(Usuario, id=user_id)
        user_json = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "address": user.address,
            "company": user.company,
            "date_birth": user.date_birth
        }
        return JsonResponse(user_json, status=200)
    else:
        return HttpResponseNotAllowed()


def date_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
