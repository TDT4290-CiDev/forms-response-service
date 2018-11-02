from flask import Flask, jsonify, request
from pymongo import MongoClient
from form_response_collection import FormResponseCollection


app = Flask(__name__)

form_response_collection = FormResponseCollection()


@app.route('/', methods=['GET'])
def get_all_forms():
    forms = form_response_collection.get_all_forms()
    return jsonify({'all_forms': forms})


@app.route('/<id>', methods=['GET'])
def get_one_form(id):
    try:
        form = form_response_collection.get_form_by_id(id)
        return jsonify({'form': form})

    except ValueError:
        return jsonify({'message': 'form does not exist'}), 404


@app.route('/', methods=['POST'])
def add_form():
    try:
        form = request.get_json()
        form_response_collection.add_form(form)
        return jsonify({'message': 'Successfully inserted document'}), 201

    except ValueError:
        return jsonify({'message': 'Credentials not provied'}), 401


@app.route('/<id>', methods=['PUT'])
def update_one_form(id):
    try:
        updates = request.get_json()
        form_response_collection.update_one_form(id, updates)

    except ValueError:
        return jsonify({'message': 'form does not exist'}), 404


@app.route('/<id>', methods=['DELETE'])
def delete_one_form(id):
    try:
        form_response_collection.delete_form_by_id(id)

        return jsonify({'message': 'form successfully deleted'}), 200
    except ValueError:
        return jsonify({'message': 'form does not exist'}), 404


if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=8080)
 



