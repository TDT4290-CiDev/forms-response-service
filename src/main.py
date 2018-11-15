from flask import Flask, jsonify, request
from form_response_collection import FormResponseCollection
from http import HTTPStatus


app = Flask(__name__)
form_response_collection = FormResponseCollection()


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

    except ValueError:
        return 'Form does not exist', HTTPStatus.NOT_FOUND


@app.route('/<form_id>', methods=['POST'])
def add_response(form_id):
    response = request.get_json()
    rid = form_response_collection.add_response(form_id, response)
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
