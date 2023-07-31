from bson import ObjectId

class SearchResultRepository:
    def __init__(self, mongo_client):
        self.mongo_client = mongo_client
        self.collection = mongo_client.collection

    def get_by_id(self, id):
        id = ObjectId(id)
        search_result = self.collection.find_one({"_id": id})
        return search_result
