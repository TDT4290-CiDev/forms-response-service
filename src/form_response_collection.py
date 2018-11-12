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
        self.form_response_collection.create_index('workflows', name='workflows-index')

    def get_form_by_id(self, rid):
        form = self.form_response_collection.find_one(ObjectId(rid))
        if not form:
            raise ValueError

        form['_id'] = str(form['_id'])
        return form

    def get_all_forms(self):
        forms = self.form_response_collection.find({})
        result = []
        for form in forms:
            form['_id'] = str(form['_id'])
            result.append(form)

        return result

    def add_form(self, form):
        rid = self.form_response_collection.insert_one(form).inserted_id
        return str(rid)

    def update_one_form(self, rid, updates):
        if not self.form_response_collection.find_one(ObjectId(rid)):
            raise ValueError
        self.form_response_collection.update_one(ObjectId(rid), {'$set': updates})

    def delete_all_forms(self):
        self.form_response_collection.delete_many({})

    def delete_form_by_id(self, rid):
        self.form_response_collection.delete_one({'_id': ObjectId(rid)})


form = FormResponseCollection()

