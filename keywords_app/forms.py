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
            "congreso_search": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input create-congreso-checkboxes"}),
            "estatal_search": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input create-estatal-checkboxes"})
        }

        labels = {
            "first_keyword": _("Keyword 1"),
            "second_keyword": _("Keyword 2"),
            "congreso_search": _("Congreso:"),
            "estatal_search": _("Estatal:"),
        }


class EditKeywordForm(KeywordForm):

    class Meta(KeywordForm.Meta):
        widgets = {
            "first_keyword": forms.TextInput(attrs={"class": "form-control", "id": "id_edit_first_keyword"}),
            "second_keyword": forms.TextInput(attrs={"class": "form-control", "id": "id_edit_second_keyword"}),
            "congreso_search": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input edit-congreso-checkboxes", "id": "id_edit_congreso_search"}),
            "estatal_search": forms.CheckboxSelectMultiple(attrs={"class": "edit-estatal-checkboxes form-check-input", "id": "id_edit_estatal_search"}),
        }
