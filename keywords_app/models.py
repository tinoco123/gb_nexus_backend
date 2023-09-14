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
        States, related_name="estatal_search", blank=True)
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

    def set_statal_states(self):
        estatal_states = tuple(
            self.estatal_search.all().values_list("state", flat=True))
        query_estatal = {
            "$and": [
                {"state": {"$in": estatal_states}},
                {"federalEstatal": "Estatal"}
            ]}
        return query_estatal

    def set_congreso_states(self):
        congreso_states = tuple(
            self.congreso_search.all().values_list("state", flat=True))
        query_congreso = {
            "$and": [
                {"state": {"$in": congreso_states}},
                {"federalEstatal": "Congreso"}
            ]}
        return query_congreso

    def set_federal_dependencies(self):
        federal_list = tuple(
            self.federal_search.all().values_list("federal", flat=True))
        query_federal = {
            "$and": [
                {"state": {"$in": federal_list}},
                {"federalEstatal": "Federal"}
            ]}
        return query_federal

    def query(self):
        full_query = {}

        required_search_terms = self.set_required_search_terms()

        not_required_search_terms = self.set_no_required_search_terms()

        search_terms_subquery = {}
        if not_required_search_terms:
            search_terms_subquery = {"$or": [
                required_search_terms,
                not_required_search_terms
            ]}
        else:
            search_terms_subquery = required_search_terms

        estatal_states_number = self.estatal_search.count()
        congreso_states_number = self.congreso_search.count()
        federal_number = self.federal_search.count()
        add_where_to_search = []

        if estatal_states_number >= 1:
            add_where_to_search.append(self.set_statal_states())

        if congreso_states_number >= 1:
            add_where_to_search.append(self.set_congreso_states())

        if federal_number >= 1:
            add_where_to_search.append(self.set_federal_dependencies())

        if len(add_where_to_search) == 0:
            full_query.update(search_terms_subquery)

        elif len(add_where_to_search) == 1:
            subquery = {
                "$and": [
                    search_terms_subquery,
                    add_where_to_search[0]
                ]
            }
            full_query.update(subquery)
        else:
            subquery = {
                "$and": [
                    search_terms_subquery,
                    {"$or": []}
                ]
            }
            for element in add_where_to_search:
                full_query["$and"][1]["$or"].append(element)
            full_query.update(subquery)
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
