from flask import Flask, jsonify, request
from form_response_collection import FormResponseCollection
from http import HTTPStatus

import requests


app = Flask(__name__)
form_response_collection = FormResponseCollection()
form_editor_url = 'http://form-editor-service:8080/'
case_executor_url = 'http://case-executor-service:8080/'


@app.route('/', methods=['GET'])
@app.route('/<form_id>')
def get_all_responses(form_id=None):
    if form_id is None:
        responses = form_response_collection.get_all_responses()
    else:
        responses = form_response_collection.get_responses_to_form(form_id)
    return jsonify({'data': responses})


@app.route('/<rid>', methods=['GET'])
def get_one_response(rid):
    try:
        response = form_response_collection.get_response_by_id(rid)
        return jsonify({'data': response})

    except ValueError:
        return 'Form does not exist', HTTPStatus.NOT_FOUND


@app.route('/<form_id>', methods=['POST'])
def add_response(form_id):
    form_request = requests.get(form_editor_url + form_id)

    if form_request.status_code == 404:
        return 'No form with id {} exists'.format(form_id), HTTPStatus.BAD_REQUEST

    form = form_request.json()
    response = request.get_json()

    if 'workflows' in form:
        for flow in form['workflows']:
            requests.post(case_executor_url + 'execute_workflow/' + flow, json=response)

    rid = form_response_collection.add_response(response, form_id)
    return rid, HTTPStatus.CREATED


@app.route('/<rid>', methods=['PUT'])
def update_one_response(rid):
    try:
        updates = request.get_json()
        form_response_collection.update_one_response(rid, updates)

    except ValueError:
        return 'Form does not exist', HTTPStatus.NOT_FOUND


@app.route('/<rid>', methods=['DELETE'])
def delete_one_response(rid):
    try:
        form_response_collection.delete_response_by_id(rid)

        return 'Form successfully deleted', HTTPStatus.OK
    except ValueError:
        return 'Form does not exist', HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
