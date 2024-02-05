from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.http import HttpResponseNotAllowed, JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils import timezone
from tipos_usuarios.models import Cliente
from .forms import ClientForm, EditClientForm
from usuarios_app.utils import DateJSONEnconder
from datetime import timedelta


@login_required
@permission_required("tipos_usuarios.view_cliente", raise_exception=True)
def clients(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        create_client_form = ClientForm()
        edit_client_form = EditClientForm()
        return render(request, "clients.html", {"create_client_form": create_client_form, "edit_client_form": edit_client_form})


@login_required
@permission_required("tipos_usuarios.view_cliente", raise_exception=True)
def paginate_clients(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            page_number = int(request.GET.get("page"))
            page_size = int(request.GET.get("size"))
            if request.user.user_type == "ADMINISTRADOR":
                clients_queryset = Cliente.objects.all().values("id", "first_name", "last_name",
                                                                "email", "company", "last_login", "date_joined").order_by("-id")
            else:
                clients_queryset = Cliente.objects.filter(created_by=request.user.id).values(
                    "id", "first_name", "last_name", "email", "company", "last_login", "date_joined").order_by("-id")

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

            return JsonResponse(clients_response, encoder=DateJSONEnconder)

        except ValueError:
            return HttpResponseBadRequest("Los parámetros enviados son inválidos")
        except EmptyPage:
            if page_number < 1:
                return HttpResponseBadRequest("El número de la página es menor que 1")
            else:
                return HttpResponseBadRequest("La página solicitada no contiene resultados")
        except TypeError:
            return HttpResponseBadRequest("Los parámetros page y size no deben ser omitidos")


@login_required
@permission_required("tipos_usuarios.add_cliente", raise_exception=True)
def create_client(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        client_form = ClientForm(request.POST)
        if client_form.is_valid():
            email = client_form.cleaned_data["email"]
            password = client_form.cleaned_data["password"]
            first_name = client_form.cleaned_data["first_name"]
            last_name = client_form.cleaned_data["last_name"]
            address = client_form.cleaned_data["address"]
            company = client_form.cleaned_data["company"]
            date_birth = client_form.cleaned_data["date_birth"]
            Cliente.objects.create(email=email, password=password, first_name=first_name,
                                   last_name=last_name, address=address, company=company, date_birth=date_birth, created_by=request.user.id)
            return JsonResponse({}, status=200)
        else:
            errors = client_form.errors.as_json(escape_html=True)
            return JsonResponse({'success': False, 'errors': errors}, status=400)


@login_required
@permission_required("tipos_usuarios.view_cliente", raise_exception=True)
def get_client(request, client_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        user = get_object_or_404(Cliente, id=client_id)
        if request.user.user_type == "USUARIO":
            if user.created_by != request.user.id:
                return JsonResponse({"success": False, "error": "No puedes obtener clientes que no has creado"}, status=403)

        user_json = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "address": user.address,
            "company": user.company,
            "date_birth": user.date_birth,
            "is_active": user.is_active,
        }
        return JsonResponse(user_json, status=200)


@login_required
@permission_required("tipos_usuarios.change_cliente", raise_exception=True)
def edit_client(request, client_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        user = get_object_or_404(Cliente, id=client_id)
        if request.user.user_type == "USUARIO":
            if user.created_by != request.user.id:
                return JsonResponse({"success": False, "error": "No puedes editar clientes que no has creado"}, status=403)
        edit_client_form = EditClientForm(request.POST, instance=user)
        if edit_client_form.is_valid():
            email = edit_client_form.cleaned_data["email"]
            password = edit_client_form.cleaned_data["password"]
            first_name = edit_client_form.cleaned_data["first_name"]
            last_name = edit_client_form.cleaned_data["last_name"]
            address = edit_client_form.cleaned_data["address"]
            company = edit_client_form.cleaned_data["company"]
            date_birth = edit_client_form.cleaned_data["date_birth"]
            is_active = edit_client_form.cleaned_data["is_active"]
            Cliente.objects.edit(id=client_id, email=email, password=password, first_name=first_name,
                                 last_name=last_name, address=address, company=company, date_birth=date_birth, is_active=is_active)
            return JsonResponse({}, status=200)
        else:
            errors = edit_client_form.errors.as_json(escape_html=True)
            return JsonResponse({'success': False, 'errors': errors}, status=400)


@login_required
@permission_required("tipos_usuarios.change_cliente", raise_exception=True)
def delete_client(request, client_id):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(permitted_methods=("DELETE"))
    else:
        user = get_object_or_404(Cliente, id=client_id)
        if request.user.user_type == "USUARIO":
            if user.created_by != request.user.id:
                return JsonResponse({"success": False, "error": "No puedes eliminar clientes que no has creado"}, status=403)
        if user is not None:
            user.delete()
            return JsonResponse({"response": "El usuario fue eliminado correctamente"}, status=200)


@login_required
def set_mail_frequency(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        client_id = request.user.id
        client = get_object_or_404(Cliente, id=client_id)

        today_date = timezone.now().date()

        frequency_selected = request.POST.get("frecuency-emails", "")
        if frequency_selected == "custom":
            custom_frequency = int(request.POST.get("custom-day-frequency"))
            if custom_frequency > 30 or custom_frequency < 1:
                messages.error(request, "La frecuencia debe estar en un rango de 1 a 30 días")
            else:
                client.mail_frequency = custom_frequency
                client.next_mail = today_date + timedelta(days=custom_frequency)
                messages.success(request, "Mails personalizados configurados correctamente")
        elif frequency_selected == "1":
            client.mail_frequency = 1
            client.next_mail = today_date + timedelta(days=1)
            messages.success(request, "Mails diarios configurados correctamente")
        elif frequency_selected == "7":
            client.mail_frequency = 7
            client.next_mail = today_date + timedelta(days=7)
            messages.success(request, "Mails semanales configurados correctamente")
        client.save()
        return redirect("keywords") 