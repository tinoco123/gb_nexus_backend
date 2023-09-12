from django.db import models
from tipos_usuarios.models import UserBaseAccount


from django.db import models


class States(models.Model):
    state = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.state


class Federal(models.Model):
    federal = models.CharField(max_length=31, unique=True)

    def __str__(self):
        return self.federal


class Keyword(models.Model):
    congreso_search = models.ManyToManyField(States)
    estatal_search = models.ManyToManyField(
        States, related_name="estatal_search")
    federal_search = models.ManyToManyField(Federal)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        UserBaseAccount, on_delete=models.CASCADE, null=False)

    def to_json(self):
        keyword_json = {
            "congreso_search": list(self.congreso_search.all().values_list("id", flat=True)),
            "estatal_search": list(self.estatal_search.all().values_list("id", flat=True)),
            "federal_search": list(self.federal_search.all().values_list("id", flat=True)),
            "search_terms": list(self.searchterms_set.all().values("id", "name", "is_required"))
        }
        return keyword_json

    def query(self):
        estatal_states_number = self.estatal_search.count()

        if estatal_states_number >= 1:
            estatal_states = list(
                self.estatal_search.all().values_list("state", flat=True))
            query_estatal = {
                "$and": [
                    {"state": {"$regex": "|".join(
                        estatal_states), "$options": "i"}},
                    {"federalEstatal": "Estatal"}
                ]}
        congreso_states_number = self.congreso_search.count()
        if congreso_states_number >= 1:
            congreso_states = list(
                self.congreso_search.all().values_list("state", flat=True))
            query_congreso = {
                "$and": [
                    {"state": {"$regex": "|".join(
                        congreso_states), "$options": "i"}},
                    {"federalEstatal": "Congreso"}
                ]}
        federal_number = self.federal_search.count()
        if federal_number >= 1:
            federal_list = list(
                self.federal_search.all().values_list("federal", flat=True))
            query_federal = {
                "$and": [
                    {"federal": {"$regex": "|".join(
                        federal_list), "$options": "i"}},
                    {"federalEstatal": "Federal"}
                ]}
        
        where_search = {
            "$or": [
                query_estatal,
                query_congreso,
                query_federal
            ]
        }
        print(where_search)
        return where_search
    



class SearchTerms(models.Model):
    name = models.CharField(max_length=30)
    is_required = models.BooleanField()
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)

    def to_json(self):
        search_term_json = {
            "name": self.name,
            "is_required": self.is_required,
            "keyword_id": self.keyword.id
        }
        return search_term_json
