from bson import ObjectId


class SearchResultRepository:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
        self.collection = mongo_client.collection

    def get_by_id(self, id):
        id = ObjectId(id)
        search_result = self.collection.find_one(
            {"_id": id}, {"sinopsys": 1, "urlAttach": 1})
        return search_result

    def get_document_for_pdf(self, id):
        id = ObjectId(id)
        search_result = self.collection.find_one(
            {"_id": id}, {"_id": 0, "collectionName": 0, "image":0, "legislature": 0})
        return search_result

    def count_results(self, query: dict):
        results = self.collection.count_documents(query)
        return results
