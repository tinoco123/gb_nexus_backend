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
    congreso_search  = models.ManyToManyField(States)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        UserBaseAccount, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.first_keyword

    def to_json(self):
        keyword_json = {
            "first_keyword": self.first_keyword,
            "second_keyword": self.second_keyword,
            "congreso_search": list(self.congreso_search.all().values_list("id", flat=True))
        }
        return keyword_json

    def query(self):
        query_keywords = {}
        if self.second_keyword:
            query_keywords = {"$regex": "|".join(
                (self.first_keyword, self.second_keyword)), "$options": "i"}
        else:
            query_keywords = {"$regex": self.first_keyword, "$options": "i"}

        congreso_states = tuple(self.congreso_search.all().values_list("state", flat=True))
        query_states = {}
        if len(congreso_states) == 1:
            query_states = {"$regex": "".join(congreso_states), "$options": "i"}
        else:
            query_states = {"$regex": "|".join(congreso_states), "$options": "i"}

        query = {
            "$and": [
                {
                    "$or": [
                        {"sinopsys": query_keywords},
                        {"urlAttach.sinopsys": query_keywords}
                    ]
                },
                {"state": query_states}
            ]
        }
        return query
