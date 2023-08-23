from django import forms
from .models import Keyword
from django.utils.translation import gettext_lazy as _


class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        exclude = ['date_created', 'user']

        widgets = {
            "first_keyword": forms.TextInput(attrs={"class": "form-control"}),
            "second_keyword": forms.TextInput(attrs={"class": "form-control"}),
            "states_to_search": forms.SelectMultiple(attrs={"class": "form-select form-select-sm"})
        }

        labels = {
            "first_keyword": _("Keyword 1"),
            "second_keyword": _("Keyword 2"),
            "states_to_search": _("Buscar en:"),
        }
