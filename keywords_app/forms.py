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
            "states_to_search": forms.SelectMultiple(attrs={"class": "form-select"})
        }

        labels = {
            "first_keyword": _("Keyword 1"),
            "second_keyword": _("Keyword 2"),
            "states_to_search": _("Buscar en:"),
        }


class EditKeywordForm(KeywordForm):

    class Meta(KeywordForm.Meta):
        widgets = {
            "first_keyword": forms.TextInput(attrs={"class": "form-control", "id": "id_edit_first_keyword"}),
            "second_keyword": forms.TextInput(attrs={"class": "form-control", "id": "id_edit_second_keyword"}),
            "states_to_search": forms.SelectMultiple(attrs={"class": "form-select", "id": "id_edit_states_to_search"})
        }
