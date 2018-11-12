from flask import Flask, jsonify, request
from form_response_collection import FormResponseCollection
from http import HTTPStatus


app = Flask(__name__)
form_response_collection = FormResponseCollection()


@app.route('/', methods=['GET'])
@app.route('/<form_id>')
def get_all_forms(form_id=None):
    if form_id is None:
        forms = form_response_collection.get_all_responses()
    else:
        forms = form_response_collection.get_responses_to_form(form_id)
    return jsonify({'data': forms})


@app.route('/<rid>', methods=['GET'])
def get_one_form(rid):
    try:
        form = form_response_collection.get_response_by_id(rid)
        return jsonify({'data': form})

    except ValueError:
        return 'Form does not exist', HTTPStatus.NOT_FOUND


@app.route('/', methods=['POST'])
def add_form():
    form = request.get_json()
    rid = form_response_collection.add_response(form)
    return rid, HTTPStatus.CREATED


@app.route('/<rid>', methods=['PUT'])
def update_one_form(rid):
    try:
        updates = request.get_json()
        form_response_collection.update_one_response(rid, updates)

    except ValueError:
        return 'Form does not exist', HTTPStatus.NOT_FOUND


@app.route('/<rid>', methods=['DELETE'])
def delete_one_form(rid):
    try:
        form_response_collection.delete_response_by_id(rid)

        return 'Form successfully deleted', HTTPStatus.OK
    except ValueError:
        return 'Form does not exist', HTTPStatus.NOT_FOUND


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
