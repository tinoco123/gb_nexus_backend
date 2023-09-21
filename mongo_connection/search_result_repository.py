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

    def get_url_attach_by_id(self, id):
        id = ObjectId(id)
        urlAttach = self.collection.find_one({"_id": id}, {"urlAttach": 1})
        return urlAttach
