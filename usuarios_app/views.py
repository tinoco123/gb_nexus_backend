from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from .forms import UserForm
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
                Usuario.objects.create_user(email=email, password=password, first_name=first_name,
                                            last_name=last_name, address=address, company=company, date_birth=date_birth)
                return redirect("users")
            else:
                errors = user_form.errors.as_json(escape_html=True)
                return JsonResponse({'success': False, 'errors': errors}, status=400)
        else:
            return redirect("users")


def date_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
