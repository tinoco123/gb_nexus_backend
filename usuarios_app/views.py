from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from tipos_usuarios.models import Usuario
from datetime import date, datetime
import json


@login_required
def users(request):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()
    else:
        if request.method == "GET":
            users = list(Usuario.objects.values(
                "id", "first_name", "last_name", "company", "date_joined"))
            usuarios_json = json.dumps(users, default=date_serializer)
            return render(request, 'usuarios.html', {"users": usuarios_json})


def date_serializer(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))
