from django import forms
from tipos_usuarios.models import Usuario
from django.utils.translation import gettext_lazy as _


class UserForm(forms.ModelForm):
    class Meta:
        model = Usuario
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


class EditUserForm(UserForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False
    
    class Meta(UserForm.Meta):
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "id": "id_edit_email"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "id": "id_edit_password"}),
            "first_name": forms.TextInput(attrs={"class": "form-control", "id": "id_edit_first_name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "id": "id_edit_last_name"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 4, "id": "id_edit_address"}),
            "company": forms.TextInput(attrs={"class": "form-control", "id": "id_edit_company"}),
            "date_birth": forms.DateInput(attrs={"class": "form-control", "type": "date", "id": "id_edit_date_birth"})
        }
