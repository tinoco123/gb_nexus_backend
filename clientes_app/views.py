from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from tipos_usuarios.models import Cliente
from .forms import ClientForm, EditClientForm

@login_required
def clients(request):
    if request.user.user_type == "CLIENTE":
        return HttpResponseForbidden("No tienes autorización para acceder a este recurso")
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        create_client_form = ClientForm()
        edit_client_form = EditClientForm()
        return render(request, "clients.html", {"create_client_form": create_client_form, "edit_client_form": edit_client_form})


@login_required
def all_clients(request):
    if request.user.user_type == "CLIENTE":
        return HttpResponseForbidden("No tienes autorización para acceder a este recurso")
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        clients_queryset = Cliente.objects.all().values("id", "first_name", "last_name",
                                                        "email", "company", "date_joined").order_by("id")
        clients_data = list(clients_queryset)
        return JsonResponse(clients_data, safe=False)


@login_required
def paginate_clients(request):
    if request.user.user_type == "CLIENTE":
        return HttpResponseForbidden("No tienes autorización para acceder a este recurso")
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            page_number = int(request.GET.get("page"))
            page_size = int(request.GET.get("size"))
            clients_queryset = Cliente.objects.all().values("id", "first_name", "last_name",
                                                            "email", "company", "date_joined").order_by("id")
            if page_size > 50 or page_size < 10:
                return HttpResponseBadRequest("El número de elementos a retornar es inválido. Debe ser mayor a mayor o igual que 10 y menor e igual que 50")

            paginator = Paginator(clients_queryset, page_size)

            if page_number > paginator.num_pages or page_number < 1:
                return HttpResponseBadRequest("El número de página solicitado es inválido")

            selected_page = paginator.page(page_number)
            clients_response = {
                "last_page": paginator.num_pages,
                "data": list(selected_page.object_list)
            }

            return JsonResponse(clients_response)

        except ValueError:
            return HttpResponseBadRequest("Los parámetros enviados son inválidos")
        except EmptyPage:
            if page_number < 1:
                return HttpResponseBadRequest("El número de la página es menor que 1")
            else:
                return HttpResponseBadRequest("La página solicitada no contiene resultados")
        except TypeError:
            return HttpResponseBadRequest("Los parámetros page y size no deben ser omitidos")
