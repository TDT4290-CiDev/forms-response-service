from bson.objectid import ObjectId, InvalidId



def catch_invalid_id(form_operator):
    def catch_wrapper(*args):
        try:
            return form_operator(*args)
        except InvalidId:
            raise ValueError('{} is not a valid ID. '.format(args[1]))
    return catch_wrapper


class FormResponseCollection:

    client = None
    db = None
    form_response_collection = None

    def __init__(self, client):
        self.client = client
        self.db = self.client.cidev_db
        self.form_response_collection = self.db.form_response_collection
        self.form_response_collection.create_index('_form', name='form-index')

    @catch_invalid_id
    def get_response_by_id(self, rid):
        response = self.form_response_collection.find_one(ObjectId(rid))
        if not response:
            raise ValueError(f'Form response with id {rid} does not exist.')

        response['_id'] = str(response['_id'])
        response['_form'] = str(response['_form'])
        return response

    def get_all_responses(self):
        responses = self.form_response_collection.find({})
        result = []
        for response in responses:
            response['_id'] = str(response['_id'])
            response['_form'] = str(response['_form'])
            result.append(response)

        return result

    @catch_invalid_id
    def get_responses_to_form(self, form_id):
        responses = self.form_response_collection.find({'_form': ObjectId(form_id)})
        result = []
        for response in responses:
            response['_id'] = str(response['_id'])
            response['_form'] = str(response['_form'])
            result.append(response)

        return result

    @catch_invalid_id
    def add_response(self, form_id, response):
        response['_form'] = ObjectId(form_id)
        rid = self.form_response_collection.insert_one(response).inserted_id
        return str(rid)

    @catch_invalid_id
    def update_one_response(self, rid, updates):
        update_res = self.form_response_collection.update_one({'_id': ObjectId(rid)}, {'$set': updates})
        if update_res.matched_count == 0:
            raise ValueError(f'Form response with id {rid} does not exist.')

    def delete_all_responses(self):
        self.form_response_collection.delete_many({})

    @catch_invalid_id
    def delete_response_by_id(self, rid):
        delete_res = self.form_response_collection.delete_one({'_id': ObjectId(rid)})
        if delete_res.deleted_count == 0:
            raise ValueError(f'Form response with id {rid} does not exist.')
