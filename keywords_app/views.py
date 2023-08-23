from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage
from keywords_app.models import Keyword
from .forms import KeywordForm
from tipos_usuarios.models import UserBaseAccount
from django.contrib.auth.decorators import login_required


@login_required
def keywords(request):
    keyword_form = KeywordForm()
    return render(request, 'keywords.html', {"create_keyword_form": keyword_form})


@login_required
def create_keyword(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("No tienes autorización para acceder a este recurso")
    if request.method != "POST":
        return HttpResponseNotAllowed(permitted_methods=("POST"))
    else:
        keyword_form = KeywordForm(request.POST)
        if keyword_form.is_valid():
            keyword = keyword_form.save(commit=False)
            keyword.user = get_object_or_404(
                UserBaseAccount, pk=request.user.id)
            keyword.save()
            keyword.states_to_search.set(
                keyword_form.cleaned_data["states_to_search"])
            return JsonResponse({"success": True, "status_text": "Cliente añadido correctamente"}, status=200)
        else:
            errors = keyword_form.errors.as_json(escape_html=True)
            return JsonResponse({'success': False, 'errors': errors}, status=400)


@login_required
def paginate_keywords(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("No tienes autorización para acceder a este recurso")
    if request.method != "GET":
        return HttpResponseNotAllowed(permitted_methods=("GET"))
    else:
        try:
            page_number = int(request.GET.get("page"))
            page_size = int(request.GET.get("size"))
            
            keywords_queryset = Keyword.objects.all().values("id", "first_keyword", "second_keyword", "date_created").order_by("id")
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