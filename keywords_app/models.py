from django.db import models
from tipos_usuarios.models import UserBaseAccount


from django.db import models


class States(models.Model):
    state = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.state


class Keyword(models.Model):
    first_keyword = models.CharField(max_length=50, null=False, blank=False)
    second_keyword = models.CharField(max_length=50, null=True, blank=True)
    states_to_search = models.ManyToManyField(States)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        UserBaseAccount, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.first_keyword

    def to_json(self):
        keyword_json = {
            "first_keyword": self.first_keyword,
            "second_keyword": self.second_keyword,
            "states_to_search": list(self.states_to_search.all().values("state"))
        }
        return keyword_json
