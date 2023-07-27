from connection import MongoConnection
from pymongo import ASCENDING


class Pagination:
    def __init__(self, page_size, db, collection):
        self.connection = MongoConnection(db, collection)
        self.page_size = page_size
        self.last_page = self.calc_last_page()

    def get_page(self, page_number):
        skip_value = (page_number - 1) * self.page_size
        documents = self.connection.collection.find({}, {"_id": 1, "title": 1}).sort(
            "_id", ASCENDING).skip(skip_value).limit(self.page_size)
        documents = (document for document in documents)
        return documents

    def calc_last_page(self):
        estimated_data = self.connection.collection.estimated_document_count()
        if estimated_data % 2 == 0:
            last_page = estimated_data // self.page_size
        else:
            last_page = (estimated_data // self.page_size) + 1

        return last_page
