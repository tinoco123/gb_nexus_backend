from django.db import models
from tipos_usuarios.models import UserBaseAccount


from django.db import models


class States(models.Model):
    state = models.CharField(max_length=30 ,unique=True)


class Keyword(models.Model):
    first_keyword = models.CharField(max_length=50, null=False, blank=False)
    second_keyword = models.CharField(max_length=50, null=True, blank=True)
    states_to_search = models.ManyToManyField(States)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserBaseAccount, on_delete=models.CASCADE, null=False)
