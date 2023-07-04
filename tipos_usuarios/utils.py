from django.db import models

class UserTypes(models.TextChoices):
    ADMINISTRADOR = "ADMINISTRADOR", "Administrador"
    USUARIO = "USUARIO", "Usuario"
    CLIENTE = "CLIENTE", "Cliente"