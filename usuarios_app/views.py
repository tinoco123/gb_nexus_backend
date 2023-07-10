from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from tipos_usuarios.models import Usuario

@login_required
def users(request):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()
    else:
        if request.method == "GET":
            return render(request, 'usuarios.html')


@login_required
def get_users(request):
    if not request.user.user_type == "ADMINISTRADOR":
        return HttpResponseForbidden()
    else:
        users = list(Usuario.objects.all().values("id" , "first_name", "last_name", "company", "date_joined"))
        return JsonResponse(users, safe=False)