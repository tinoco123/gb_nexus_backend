from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage
from keywords_app.models import Keyword
from .forms import KeywordForm, EditKeywordForm
from tipos_usuarios.models import UserBaseAccount
from django.contrib.auth.decorators import login_required


@login_required
def keywords(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        keyword_form = KeywordForm()
        edit_keyword_form = EditKeywordForm()
        return render(request, 'keywords.html', {"create_keyword_form": keyword_form, "edit_keyword_form": edit_keyword_form})


@login_required
def create_keyword(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        keyword_form = KeywordForm(request.POST)
        if keyword_form.is_valid():
            keyword = keyword_form.save(commit=False)
            keyword.user = get_object_or_404(
                UserBaseAccount, pk=request.user.id)
            keyword.save()
            keyword.congreso_search.set(
                keyword_form.cleaned_data["congreso_search"])
            keyword.estatal_search.set(
                keyword_form.cleaned_data["estatal_search"])
            keyword.federal_search.set(
                keyword_form.cleaned_data["federal_search"])
            return JsonResponse({"success": True, "status_text": "Keyword añadido correctamente"}, status=200)
        else:
            errors = keyword_form.errors.as_json(escape_html=True)
            return JsonResponse({'success': False, 'errors': errors}, status=400)


@login_required
def paginate_keywords(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            page_number = int(request.GET.get("page"))
            page_size = int(request.GET.get("size"))
            user = get_object_or_404(UserBaseAccount, pk=request.user.id)
            if request.user.user_type == "ADMINISTRADOR":
                keywords_queryset = Keyword.objects.all().values(
                    "id", "searchterms", "date_created").order_by("id")
                print(keywords_queryset)
            else:
                keywords_queryset = Keyword.objects.filter(user=user).values(
                    "id", "date_created").order_by("id")
            if page_size > 50 or page_size < 10:
                return HttpResponseBadRequest("El número de elementos a retornar es inválido. Debe ser mayor a mayor o igual que 10 y menor e igual que 50")

            paginator = Paginator(keywords_queryset, page_size)

            if page_number > paginator.num_pages or page_number < 1:
                return HttpResponseBadRequest("El número de página solicitado es inválido")

            selected_page = paginator.page(page_number)
            keywords_response = {
                "last_page": paginator.num_pages,
                "data": list(selected_page.object_list)
            }

            return JsonResponse(keywords_response)

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
def get_keyword(request, keyword_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        keyword = get_object_or_404(Keyword, id=keyword_id)
        if keyword.user.id == request.user.id or request.user.user_type == "ADMINISTRADOR":
            return JsonResponse(keyword.to_json(), safe=False)
        else:
            return JsonResponse({'success': False, 'errors': "No puedes obtener una keyword de otro usuario"}, status=403)


@login_required
def edit_keyword(request, keyword_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        keyword = get_object_or_404(Keyword, id=keyword_id)
        if keyword.user.id != request.user.id and request.user.user_type != "ADMINISTRADOR":
            return JsonResponse({'success': False, 'errors': "No puedes editar una keyword de otro usuario"}, status=403)
        edit_keyword_form = EditKeywordForm(request.POST, instance=keyword)
        if edit_keyword_form.is_valid():
            keyword = edit_keyword_form.save()
            keyword.congreso_search.set(edit_keyword_form.cleaned_data["congreso_search"])
            keyword.estatal_search.set(edit_keyword_form.cleaned_data["estatal_search"])
            keyword.federal_search.set(edit_keyword_form.cleaned_data["federal_search"])
            return JsonResponse({"success": True, "status_text": "Keyword editado correctamente"}, status=200)
        else:
            errors = edit_keyword_form.errors.as_json(escape_html=True)
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        

@login_required
def delete_keyword(request, keyword_id):
    if request.method != "DELETE":
        return HttpResponseNotAllowed(permitted_methods=("DELETE"))
    else:
        keyword = get_object_or_404(Keyword, id=keyword_id)
        if keyword.user.id != request.user.id and request.user.user_type != "ADMINISTRADOR":
            return JsonResponse({'success': False, 'errors': "No puedes eliminar una keyword de otro usuario"}, status=403)
        else:
            keyword.delete()
            return JsonResponse({"success": True, "status_text": "Keyword editada correctamente"}, status=200)
