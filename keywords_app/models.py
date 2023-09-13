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
    congreso_search = models.ManyToManyField(States, blank=True)
    estatal_search = models.ManyToManyField(
        States, related_name="estatal_search")
    federal_search = models.ManyToManyField(Federal, blank=True)
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


    def set_required_search_terms(self):
        search_terms_required = tuple(
                self.searchterms_set.filter(is_required=True).values_list("name", flat=True))
        what_search_required = {
            "$and": []
        }
        for search_term in search_terms_required:
            subquery = {"$or": [
                {"sinopsys": {"$regex": search_term, "$options": "i"}},
                {"urlAttach.sinopsys": {"$regex": search_term, "$options": "i"}},
            ]}
            what_search_required["$and"].append(subquery)
        return what_search_required

    def set_no_required_search_terms(self):
        if self.searchterms_set.filter(is_required=False).count() >= 1:
            search_terms_no_required = tuple(
                        self.searchterms_set.filter(is_required=False).values_list("name", flat=True))
            what_search_no_required = {
                "$or": [
                    {"sinopsys": {"$regex": "|".join(
                                search_terms_no_required), "$options": "i"}},
                    {"urlAttach.sinopsys": {"$regex": "|".join(
                                search_terms_no_required), "$options": "i"}}
                ]}
        else:
            what_search_no_required = {}
        return what_search_no_required

    def query(self):
        full_query = {}

        required_search_terms = self.set_required_search_terms()
        
        not_required_search_terms = self.set_no_required_search_terms()

        if not_required_search_terms:
            subquery = {"$or": [
                required_search_terms,
                not_required_search_terms
            ]}   
        else:
            subquery = required_search_terms

        


        estatal_states_number = self.estatal_search.count()
        congreso_states_number = self.congreso_search.count()
        federal_number = self.federal_search.count()

        if not estatal_states_number and not congreso_states_number and not federal_number:

        query_estatal = {}
        query_congreso = {}
        query_federal = {}

        where_search = {
            "$or": [
                query_estatal,
                query_congreso,
                query_federal
            ]
        }
        
        if estatal_states_number >= 1:
            estatal_states = tuple(
                self.estatal_search.all().values_list("state", flat=True))
            query_estatal = {
                "$and": [
                    {"state": {"$in": estatal_states}},
                    {"federalEstatal": "Estatal"}
                ]}
        else:
            del where_search["$or"]
        if congreso_states_number >= 1:
            congreso_states = tuple(
                self.congreso_search.all().values_list("state", flat=True))
            query_congreso = {
                "$and": [
                    {"state": {"$in": congreso_states}},
                    {"federalEstatal": "Congreso"}
                ]}
        if federal_number >= 1:
            federal_list = tuple(
                self.federal_search.all().values_list("federal", flat=True))
            query_federal = {
                "$and": [
                    {"state": {"$in": federal_list}},
                    {"federalEstatal": "Federal"}
                ]}

        what_search_no_required = {}
        #  Terminos de busqueda
        
        if what_search_no_required:
            full_query = {
                "$and": [
                    {"$or": [
                        what_search_required,
                        what_search_no_required
                    ]},
                    where_search
                ]
            }
        else:
            full_query = {
                "$and": [
                    what_search_required,
                    where_search
                ]
            }
        print(full_query)
        return full_query



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
