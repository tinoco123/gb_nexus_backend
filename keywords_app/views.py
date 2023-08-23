from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404, render
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
