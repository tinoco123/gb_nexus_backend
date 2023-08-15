from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.contrib.auth.decorators import login_required
from tipos_usuarios.models import Cliente

@login_required
def clients(request):
    if request.user.user_type == "CLIENTE":
        return HttpResponseForbidden()
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        return render(request, "clients.html")

@login_required
def all_clients(request):
    if request.user.user_type == "CLIENTE":
        return HttpResponseForbidden()
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        clients_queryset = Cliente.objects.all()
        clients_data = list(clients_queryset.values("id", "first_name", "last_name", "email", "company", "date_joined"))
        return JsonResponse(clients_data, safe=False)