from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=64, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña", required=True)

    email.widget.attrs.update({"class": "form-control input-color", "placeholder": "Escribe tu email"})
    password.widget.attrs.update({"class": "form-control input-color", "placeholder": "Escribe tu contraseña"})
