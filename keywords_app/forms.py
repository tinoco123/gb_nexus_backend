from django import forms
from .models import Keyword
from django.utils.translation import gettext_lazy as _

options = [(True, "Obligatorio"), (False, "No obligatorio")]


class KeywordForm(forms.ModelForm):
    search_term_1 = forms.CharField(label="Keyword 1", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Campo obligatorio"}), required=True, min_length=2, max_length=30)
    filter_1 = forms.ChoiceField(label="Condición 1", choices=options, widget=forms.Select(
        attrs={"class": "form-select"}))

    search_term_2 = forms.CharField(
        label="Keyword 2", widget=forms.TextInput(
            attrs={"class": "form-control"}), required=False, min_length=2, max_length=30)
    filter_2 = forms.ChoiceField(label="Condición 2", choices=options, widget=forms.Select(
        attrs={"class": "form-select"}))

    search_term_3 = forms.CharField(
        label="Keyword 3", widget=forms.TextInput(
            attrs={"class": "form-control"}), required=False, min_length=2, max_length=30)
    filter_3 = forms.ChoiceField(label="Condición 3", choices=options, widget=forms.Select(
        attrs={"class": "form-select"}))

    search_term_4 = forms.CharField(
        label="Keyword 4", widget=forms.TextInput(
            attrs={"class": "form-control"}), required=False, min_length=2, max_length=30)
    filter_4 = forms.ChoiceField(label="Condición 4", choices=options, widget=forms.Select(
        attrs={"class": "form-select"}))

    search_term_5 = forms.CharField(
        label="Keyword 5", widget=forms.TextInput(
            attrs={"class": "form-control"}), required=False, min_length=2, max_length=30)
    filter_5 = forms.ChoiceField(label="Condición 5", choices=options, widget=forms.Select(
        attrs={"class": "form-select"}))

    class Meta:
        model = Keyword
        exclude = ['date_created', 'user']

        widgets = {
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título de la búsqueda"}),
            "congreso_search": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input create-congreso-checkboxes"}),
            "estatal_search": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input create-estatal-checkboxes"}),
            "federal_search": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input create-federal-checkboxes"})
        }

        labels = {
            "start_date": _("Fecha inicio"),
            "end_date": _("Fecha final"),
            "title": _("Título de la búsqueda"),
            "congreso_search": _("Buscar en congreso:"),
            "estatal_search": _("Buscar en estatal:"),
            "federal_search": _("Buscar en federal:"),
        }


class EditKeywordForm(KeywordForm):
    search_term_1 = forms.CharField(label="Keyword 1", widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": "Campo obligatorio", "id": "id_edit_search_term_1"}), required=True, min_length=2, max_length=30)
    search_term_1_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={"class": "search_terms_ids"}), required=False)

    search_term_2 = forms.CharField(
        label="Keyword 2", widget=forms.TextInput(
            attrs={"class": "form-control", "id": "id_edit_search_term_2"}), required=False, min_length=2, max_length=30)
    search_term_2_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={"class": "search_terms_ids"}), required=False)

    search_term_3 = forms.CharField(
        label="Keyword 3", widget=forms.TextInput(
            attrs={"class": "form-control", "id": "id_edit_search_term_3"}), required=False, min_length=2, max_length=30)
    search_term_3_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={"class": "search_terms_ids"}), required=False)

    search_term_4 = forms.CharField(
        label="Keyword 4", widget=forms.TextInput(
            attrs={"class": "form-control", "id": "id_edit_search_term_4"}), required=False, min_length=2, max_length=30)
    search_term_4_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={"class": "search_terms_ids"}), required=False)

    search_term_5 = forms.CharField(
        label="Keyword 5", widget=forms.TextInput(
            attrs={"class": "form-control", "id": "id_edit_search_term_5"}), required=False, min_length=2, max_length=30)
    search_term_5_id = forms.IntegerField(
        widget=forms.HiddenInput(attrs={"class": "search_terms_ids"}), required=False)

    class Meta(KeywordForm.Meta):
        widgets = {
            "start_date": forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "id_edit_start_date"}),
            "end_date": forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "id_edit_start_date"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título de la búsqueda", "id": "id_edit_title"}),
            "congreso_search": forms.CheckboxSelectMultiple(attrs={"class": "form-check-input edit-congreso-checkboxes", "id": "id_edit_congreso_search"}),
            "estatal_search": forms.CheckboxSelectMultiple(attrs={"class": "edit-estatal-checkboxes form-check-input", "id": "id_edit_estatal_search"}),
            "federal_search": forms.CheckboxSelectMultiple(attrs={"class": "edit-federal-checkboxes form-check-input", "id": "id_edit_federal_search"}),
        }
