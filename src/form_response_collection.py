from pymongo import MongoClient
from bson.objectid import ObjectId

access_url = "forms-response-datastore:27017"


class FormResponseCollection:

    client = None
    db = None
    form_response_collection = None

    def __init__(self):
        self.client = MongoClient(access_url)
        self.db = self.client.cidev_db
        self.form_response_collection = self.db.form_response_collection
        self.form_response_collection.create_index('_form', name='form-index')

    def get_response_by_id(self, rid):
        response = self.form_response_collection.find_one(ObjectId(rid))
        if not response:
            raise ValueError

        response['_id'] = str(response['_id'])
        return response

    def get_all_responses(self):
        responses = self.form_response_collection.find({})
        result = []
        for response in responses:
            response['_id'] = str(response['_id'])
            result.append(response)

        return result

    def get_responses_to_form(self, form_id):
        responses = self.form_response_collection.find({'_form': form_id})
        result = []
        for response in responses:
            response['_id'] = str(response['_id'])
            result.append(response)

        return result

    def add_response(self, response, form_id):
        response['_form'] = form_id
        rid = self.form_response_collection.insert_one(response).inserted_id
        return str(rid)

    def update_one_response(self, rid, updates):
        if not self.form_response_collection.find_one(ObjectId(rid)):
            raise ValueError
        self.form_response_collection.update_one(ObjectId(rid), {'$set': updates})

    def delete_all_responses(self):
        self.form_response_collection.delete_many({})

    def delete_response_by_id(self, rid):
        self.form_response_collection.delete_one({'_id': ObjectId(rid)})
