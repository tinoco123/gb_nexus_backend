from bson import ObjectId
from .pipelines import get_pipeline_pdf, get_sinopsys_and_urlAttach, get_pipeline_pdf_optimized, get_base64_urlAttach_from_dof_collection, get_sinopsys_of_urlAttach_from_dof_collection


class SearchResultRepository:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
        self.collection = mongo_client.collection

    def get_by_id(self, id, keyword: str) -> dict:
        id = ObjectId(id)
        search_result = list(
            self.collection.aggregate(get_sinopsys_and_urlAttach(id, keyword)))
        return search_result[0]

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

    def get_document_for_pdf_optimized(self, query):
        search_results = self.collection.aggregate(
            get_pipeline_pdf_optimized(query))
        return search_results

    def get_base_64_string(self, id: str) -> str:
        id = ObjectId(id)
        urlAttach = list(self.collection.aggregate(
            get_base64_urlAttach_from_dof_collection(id)))
        return urlAttach[0]["urlAttach"][0]["urlAttach"]

    def get_doc_sinopsys_from_dof_collection(self, id: str) -> str:
        id = ObjectId(id)
        sinopsys = list(self.collection.aggregate(
            get_sinopsys_of_urlAttach_from_dof_collection(id)))
        return sinopsys[0]["urlAttach"][0]["sinopsys"]

    def count_results(self, query: dict):
        results = self.collection.count_documents(query)
        return results
