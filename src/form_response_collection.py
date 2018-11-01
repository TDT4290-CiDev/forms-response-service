import os
from flask import Flask, jsonify, request
from pymongo import MongoClient

access_url = os.environ['FORMS_RSPONSE_SERVICE_DATASTORE_1_PORT_27017_TCP_ADDR']
port = 27017


class FormCollection:

    client = None
    db = None
    form_collection = None

    def __init__(self):
        self.client = MongoClient(access_url, port)
        self.db = self.client.cidev_db
        self.form_collection = self.db.form_collection

    def get_form_by_id(self, id):
        form = self.form_collection.find_one({'id': id})
        if not form:
            raise ValueError

        del form['_id']
        return form

    def get_all_forms(self):
        forms = self.form_collection.find({})
        print(forms)
        result = []
        for form in forms:
            result.append(form)
        return result

    def add_form(self, form):

        self.form_collection.insert_one(form)
        return True

    def update_one_form(self, id, updates={'key1': 'arg1', 'key2': 'arg2'}):
        id = {'id': id}
        if not self.form_collection.find_one(id):
            raise ValueError
        self.form_collection.update_one(id, {'$set': updates})
        return True

    def delete_one_form(self, name, author):
        self.form_collection.delete_one({'name': name, 'author': author})
        return True

    def delete_all_forms(self):
        self.form_collection.delete_many({})
        return True

    def delete_form_by_id(self, id):
        form = self.form_collection.find_one({'id': id})
        if not form:
            raise ValueError
        self.form_collection.delete_one({'id': id})
        return True


form = FormCollection()

