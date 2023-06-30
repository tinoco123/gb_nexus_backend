from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from managers import UserBaseAccountManager


class UserBaseAccount(AbstractBaseUser):

    class Categories(models.TextChoices):
        ADMINISTRADOR = "ADMINISTRADOR", "administrador"
        USUARIO = "USUARIO", "usuario"
        CLIENTE = "CLIENTE", "cliente"

    full_name = models.CharField(max_length=127, blank=False, null=False)
    email = models.EmailField(
        max_length=64, unique=True, blank=False, null=False)
    address = models.TextField(max_length=255, blank=False, null=False)
    company = models.CharField(max_length=64, blank=True, null=True)
    category = models.CharField(
        max_length=13, choices=Categories.choices)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_birth = models.DateField(blank=False, null=False)

    is_administrador = models.BooleanField(default=False)
    is_usuario = models.BooleanField(default=False)
    is_cliente = models.BooleanField(default=False)

    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = ["email"]
    objects = UserBaseAccountManager()

    def __str__(self):
        return str(self.email)

