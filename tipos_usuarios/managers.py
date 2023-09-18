from django.db import models
from django.contrib.auth.models import BaseUserManager
from .utils import UserTypes
from django.core.exceptions import ObjectDoesNotExist
from abc import ABC, abstractmethod


class UserBaseAccountManager(BaseUserManager):
    def create(self, email, password=None, **extra_fields):
        if not email or len(email) <= 0:
            raise ValueError("El campo email es requerido")
        if not password or len(password) <= 0:
            raise ValueError("El campo contraseña es requerido")
        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, **extra_fields)


class CustomUserManager(models.Manager, ABC):

    @abstractmethod
    def create(self, email, password=None, **extra_fields):
        if not email or len(email) <= 0:
            raise ValueError("El campo email es requerido")
        if not password or len(password) <= 0:
            raise ValueError("El campo contraseña es requerido")

        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    @abstractmethod
    def edit(self, email, id, password=None, **extra_fields):
        user = self.get_queryset().get(pk=id)
        if user is not None:
            if email:
                email = BaseUserManager.normalize_email(email)
                user.email = email

            if password:
                user.set_password(password)

            for key, value in extra_fields.items():
                setattr(user, key, value)

            user.save(using=self._db)
            return user
        else:
            raise ObjectDoesNotExist()

    @abstractmethod
    def get_queryset(self, user_type, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user_type=user_type)
        return queryset


class AdministradorManager(CustomUserManager):

    def create(self, email, password=None, **extra_fields):
        super().create(email, password, **extra_fields)

    def edit(self, email, id, password=None, **extra_fields):
        super().edit(email, id, password, **extra_fields)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(user_type=UserTypes.ADMINISTRADOR, *args, **kwargs)


class UsuarioManager(CustomUserManager):

    def create(self, email, password=None, **extra_fields):
        super().create(email, password, **extra_fields)

    def edit(self, email, id, password=None, **extra_fields):
        super().edit(email, id, password, **extra_fields)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(user_type=UserTypes.USUARIO, *args, **kwargs)


class ClienteManager(CustomUserManager):

    def create(self, email, password=None, **extra_fields):
        super().create(email, password, **extra_fields)

    def edit(self, email, id, password=None, **extra_fields):
        super().edit(email, id, password, **extra_fields)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(user_type=UserTypes.CLIENTE, *args, **kwargs)
