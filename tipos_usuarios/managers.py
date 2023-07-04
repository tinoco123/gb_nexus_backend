from django.db import models
from django.contrib.auth.models import BaseUserManager
from .utils import UserTypes


class UserBaseAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email or len(email) <= 0:
            raise ValueError("El campo email es requerido")
        if not password or len(password) <= 0:
            raise ValueError("El campo contraseña es requerido")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, **extra_fields)


class AdministradorManager(models.Manager):
    def create_user(self, email, password=None, **extra_fields):
        if not email or len(email) <= 0:
            raise ValueError("El campo email es requerido")
        if not password or len(password) <= 0:
            raise ValueError("El campo contraseña es requerido")

        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user_type=UserTypes.ADMINISTRADOR)
        return queryset


class UsuarioManager(models.Manager):
    def create_user(self, email, password=None, **extra_fields):
        if not email or len(email) <= 0:
            raise ValueError("El campo email es requerido")
        if not password or len(password) <= 0:
            raise ValueError("El campo contraseña es requerido")

        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user_type=UserTypes.USUARIO)
        return queryset
