from django import forms
from tipos_usuarios.models import Cliente
from django.utils.translation import gettext_lazy as _


class ClientForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["email", "password", "first_name", "last_name",
                  "address", "company", "date_birth"]

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "date_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"})
        }
        labels = {
            "first_name": _("Nombre(s)"),
            "last_name": _("Apellidos"),
            "address": _("Dirección"),
            "company": _("Compañia"),
            "date_birth": _("Fecha de nacimiento"),
        }


class EditClientForm(ClientForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
