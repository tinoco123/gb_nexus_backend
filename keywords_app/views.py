from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage
from keywords_app.models import Keyword, SearchTerms
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

            set_search_terms_to_keyword(keyword_form, keyword)

            return JsonResponse({}, status=200)
        else:
            errors = keyword_form.errors.as_json(escape_html=True)
            return JsonResponse({'success': False, 'errors': errors}, status=400)


def set_search_terms_to_keyword(keyword_form: KeywordForm, keyword: Keyword):
    search_terms = []
    for i in range(1, 6):
        search_term = keyword_form.cleaned_data[f"search_term_{i}"]
        filter = keyword_form.cleaned_data[f"filter_{i}"]
        if search_term and filter:
            search_terms.append(SearchTerms(
                name=search_term, is_required=filter, keyword=keyword))
    SearchTerms.objects.bulk_create(search_terms)


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
                    "id", "date_created", "user").order_by("id")
            else:
                keywords_queryset = Keyword.objects.filter(user=user).values(
                    "id", "date_created").order_by("id")

            if page_size not in (10, 20, 30, 40, 50):
                return JsonResponse({"error": "El tamaño de los resultados de búsqueda debe tener alguno de los siguientes valores: 10, 20, 30, 40, 50"}, status=400)

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
            keyword.congreso_search.set(
                edit_keyword_form.cleaned_data["congreso_search"])
            keyword.estatal_search.set(
                edit_keyword_form.cleaned_data["estatal_search"])
            keyword.federal_search.set(
                edit_keyword_form.cleaned_data["federal_search"])

            set_search_terms(edit_keyword_form, keyword)

            return JsonResponse({"success": True, "status_text": "Keyword editado correctamente"}, status=200)
        else:
            errors = edit_keyword_form.errors.as_json(escape_html=True)
            return JsonResponse({'success': False, 'errors': errors}, status=400)


def set_search_terms(edit_keyword_form: EditKeywordForm, keyword: Keyword):
    for i in range(1, 6):
        search_term_id = edit_keyword_form.cleaned_data[f"search_term_{i}_id"]
        search_term_content = edit_keyword_form.cleaned_data[f"search_term_{i}"]
        is_required = edit_keyword_form.cleaned_data[f"filter_{i}"]
        if search_term_id:
            search_term_to_manipulate = get_object_or_404(
                SearchTerms, pk=search_term_id)

        if not search_term_id and not search_term_content:
            continue
        elif search_term_id and search_term_content:
            search_term_to_manipulate.name = search_term_content
            search_term_to_manipulate.is_required = is_required
            search_term_to_manipulate.save()
        elif search_term_id and not search_term_content:
            search_term_to_manipulate.delete()
        elif not search_term_id and search_term_content:
            SearchTerms.objects.create(
                name=search_term_content, is_required=is_required, keyword=keyword)


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
