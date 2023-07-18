from django.db import models
from django.contrib.auth.models import BaseUserManager
from .utils import UserTypes
from django.core.exceptions import ObjectDoesNotExist


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
    def create_administrador(self, email, password=None, **extra_fields):
        if not email or len(email) <= 0:
            raise ValueError("El campo email es requerido")
        if not password or len(password) <= 0:
            raise ValueError("El campo contraseña es requerido")

        email = BaseUserManager.normalize_email(email)
        administrador = self.model(email=email, **extra_fields)
        administrador.set_password(password)
        administrador.save(using=self._db)
        return administrador
    
    def edit_administrador(self, administrador_id, email=None, password=None, **extra_fields):
        administrador = self.get_queryset().get(pk=administrador_id)
        if administrador is not None:
            if email:
                email = BaseUserManager.normalize_email(email)
                administrador.email = email

            if password:
                administrador.set_password(password)

            for key, value in extra_fields.items():
                setattr(administrador, key, value)

            administrador.save(using=self._db)
            return administrador
        else:
            raise ObjectDoesNotExist()

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

    def edit_user(self, user_id, email=None, password=None, **extra_fields):
        user = self.get_queryset().get(pk=user_id)
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

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user_type=UserTypes.USUARIO)
        return queryset


class ClienteManager(models.Manager):
    def create_client(self, email, password=None, **extra_fields):
        if not email or len(email) <= 0:
            raise ValueError("El campo email es requerido")
        if not password or len(password) <= 0:
            raise ValueError("El campo contraseña es requerido")

        email = BaseUserManager.normalize_email(email)
        client = self.model(email=email, **extra_fields)
        client.set_password(password)
        client.save(using=self._db)
        return client

    def edit_client(self, client_id, email=None, password=None, **extra_fields):
        client = self.get_queryset().get(pk=client_id)
        if client is not None:
            if email:
                email = BaseUserManager.normalize_email(email)
                client.email = email

            if password:
                client.set_password(password)

            for key, value in extra_fields.items():
                setattr(client, key, value)

            client.save(using=self._db)
            return client
        else:
            raise ObjectDoesNotExist()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(user_type=UserTypes.CLIENTE)
        return queryset
