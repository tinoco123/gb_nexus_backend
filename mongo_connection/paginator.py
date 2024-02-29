from .connection import MongoConnection
from pymongo import DESCENDING


class Pagination:
    def __init__(self, page_size, query, mongo_client):
        self.client = mongo_client
        self.page_size = page_size
        self.query = query

    def get_page(self, page_number):
        skip_value = (page_number - 1) * self.page_size
        documents = self.client.collection.find(self.query, {"sinopsys": 0, "urlAttach": 0}).sort(
            "date", DESCENDING).skip(skip_value).limit(self.page_size)
        documents = (document for document in documents)
        return documents

    def calc_last_page(self):
        estimated_data = self.client.collection.count_documents(filter=self.query)
        if estimated_data % self.page_size == 0:
            last_page = estimated_data // self.page_size
        else:
            last_page = (estimated_data // self.page_size) + 1

        return last_page
