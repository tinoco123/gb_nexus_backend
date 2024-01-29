from bson import ObjectId
from .pipelines import get_pipeline_pdf, get_sinopsys_and_urlAttach


class SearchResultRepository:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
        self.collection = mongo_client.collection

    def get_by_id(self, id) -> dict:
        id = ObjectId(id)
        search_result = self.collection.find_one(
            {"_id": id}, {"_id": 1})
        if search_result:
            search_result = list(
                self.collection.aggregate(get_sinopsys_and_urlAttach(id)))
            return search_result[0]
        else:
            return {}

    def get_document_for_pdf(self, id):
        id = ObjectId(id)
        search_result = self.collection.find_one(
            {"_id": id}, {"_id": 1})
        if search_result:
            search_result = list(
                self.collection.aggregate(get_pipeline_pdf(id)))
            return search_result[0]
        else:
            return {}

    def get_keyword_search_results_ids(self, query: dict) -> list[dict]:
        search_results_ids = self.collection.find(query, {"_id":1})
        return search_results_ids

    def count_results(self, query: dict):
        results = self.collection.count_documents(query)
        return results
