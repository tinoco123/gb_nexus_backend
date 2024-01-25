from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserBaseAccountManager, AdministradorManager, UsuarioManager, ClienteManager
from .utils import UserTypes


class UserBaseAccount(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=127, blank=False, null=False)
    last_name = models.CharField(max_length=127, blank=False, null=False)
    email = models.EmailField(
        max_length=64, unique=True, blank=False, null=False)
    address = models.TextField(max_length=255, blank=False, null=False)
    company = models.CharField(max_length=127, blank=False, null=False)
    user_type = models.CharField(max_length=13, choices=UserTypes.choices)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_birth = models.DateField(blank=False, null=False)
    created_by = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    last_mail = models.DateField(blank=True, null=True)
    mail_frequency = models.SmallIntegerField(blank=True, null=True, default=0)

    USERNAME_FIELD = "email"
    objects = UserBaseAccountManager()

    def __str__(self):
        return str(self.email)
    
    def to_json(self):
        user_as_json = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "company": self.company,
            "last_login": self.last_login.strftime("%Y/%m/%d, %H:%M:%S"),
        }
        return user_as_json
        


class Administrador(UserBaseAccount):
    class Meta:
        proxy = True
    objects = AdministradorManager()

    def save(self, *args,  **kwargs):
        self.user_type = UserTypes.ADMINISTRADOR
        return super().save(*args,  **kwargs)


class Usuario(UserBaseAccount):
    class Meta:
        proxy = True
    objects = UsuarioManager()

    def save(self, *args,  **kwargs):
        self.user_type = UserTypes.USUARIO
        return super().save(*args,  **kwargs)


class Cliente(UserBaseAccount):
    class Meta:
        proxy = True
    objects = ClienteManager()

    def save(self, *args,  **kwargs):
        self.user_type = UserTypes.CLIENTE
        return super().save(*args,  **kwargs)
