import unittest
import mongomock
from bson.objectid import ObjectId

from form_response_collection import FormResponseCollection


class CollectionTest(unittest.TestCase):
    mock_coll = None
    initial_responses = None

    def setUp(self):
        self.example_form_id = str(ObjectId())
        self.mock_coll = FormResponseCollection(mongomock.MongoClient())
        self.initial_responses = [dict(title='response1', form='1'), dict(title='response2', form='2')]
        for f in self.initial_responses:
            f['_id'] = str(self.mock_coll.db.form_response_collection.insert_one(f).inserted_id)

    def test_add_return_valid_id(self):
        add_response = self.mock_coll.add_response(self.example_form_id, {"title": "test"})
        self.assertTrue(ObjectId.is_valid(add_response))

    def test_read_one(self):
        _id = self.initial_responses[0]['_id']
        read_response = self.mock_coll.get_response_by_id(_id)
        self.assertEqual(read_response, self.initial_responses[0])

    def test_read_all(self):
        all = self.mock_coll.get_all_responses()
        self.assertEqual(all, self.initial_responses)

    def test_update_no_return(self):
        _id = self.initial_responses[0]['_id']
        update_res = self.mock_coll.update_one_response(_id, {})
        self.assertIsNone(update_res)

    def test_delete_no_return(self):
        _id = self.initial_responses[0]['_id']
        deleteRes = self.mock_coll.delete_response_by_id(_id)
        self.assertIsNone(deleteRes)

    def test_invalid_id_format(self):
        inv_id = '0'
        with self.assertRaises(ValueError):
            self.mock_coll.get_response_by_id(inv_id)
        with self.assertRaises(ValueError):
            self.mock_coll.update_one_response(inv_id, {})
        with self.assertRaises(ValueError):
            self.mock_coll.delete_response_by_id(inv_id)

    def test_valid_but_nonexisting_id(self):
        # Creating an id of correct length, but with all 5s.
        inv_id = self.example_form_id
        with self.assertRaises(ValueError):
            self.mock_coll.get_response_by_id(inv_id)
        with self.assertRaises(ValueError):
            self.mock_coll.update_one_response(inv_id, {})
        with self.assertRaises(ValueError):
            self.mock_coll.delete_response_by_id(inv_id)
