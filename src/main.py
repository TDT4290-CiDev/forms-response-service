from http import HTTPStatus
from flask import Flask, jsonify, request
from pymongo import MongoClient

from form_response_collection import FormResponseCollection

import requests


app = Flask(__name__)

access_url = "forms-response-datastore:27017"

form_response_collection = FormResponseCollection(MongoClient(access_url))

form_editor_url = 'http://forms-editor-service:8080/'
case_executor_url = 'http://case-executor-service:8080/'


@app.route('/', methods=['GET'])
def get_all_responses():
    body = request.json()
    form_id = None
    if body and 'form' in body:
        form_id = body['form']

    if form_id is None:
        responses = form_response_collection.get_all_responses()
    else:
        try:
            responses = form_response_collection.get_responses_to_form(form_id)
        except ValueError as e:
            return str(e), HTTPStatus.BAD_REQUEST
    return jsonify({'data': responses})


@app.route('/<rid>', methods=['GET'])
def get_one_response(rid):
    try:
        response = form_response_collection.get_response_by_id(rid)
        return jsonify({'data': response})

    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


@app.route('/<form_id>', methods=['POST'])
def add_response(form_id):
    form_request = requests.get(form_editor_url + form_id)

    if form_request.status_code == HTTPStatus.NOT_FOUND:
        return 'No form with id {} exists'.format(form_id), HTTPStatus.BAD_REQUEST

    form = form_request.json()['data']
    response = request.get_json()

    if 'workflows' in form:
        for flow in form['workflows']:
            requests.post(case_executor_url + 'execute_workflow/' + flow, json=response)

    try:
        rid = form_response_collection.add_response(form_id, response)
        return rid, HTTPStatus.CREATED
    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


@app.route('/<rid>', methods=['PUT'])
def update_one_response(rid):
    try:
        updates = request.get_json()
        form_response_collection.update_one_response(rid, updates)
        return '', HTTPStatus.NO_CONTENT

    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


@app.route('/<rid>', methods=['DELETE'])
def delete_one_response(rid):
    try:
        form_response_collection.delete_response_by_id(rid)

        return '', HTTPStatus.NO_CONTENT
    except ValueError as e:
        return str(e), HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
