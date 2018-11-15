import unittest
import mongomock
from bson.objectid import ObjectId

from form_response_collection import FormResponseCollection


class CollectionTest(unittest.TestCase):
    mock_coll = None
    initial_responses = None

    def setUp(self):
        self.mock_coll = FormResponseCollection(mongomock.MongoClient())
        self.form_id_not_in_db = ObjectId()
        self.form_id_in_db = ObjectId()
        self.initial_responses = [dict(title='response1', _form=self.form_id_in_db), dict(title='response2', _form='2')]
        for f in self.initial_responses:
            f['_id'] = str(self.mock_coll.db.form_response_collection.insert_one(f).inserted_id)

    def test_add_return_valid_id(self):
        response_id = self.mock_coll.add_response(str(self.form_id_not_in_db), {"title": "test"})
        self.assertTrue(ObjectId.is_valid(response_id))

    def test_read_one(self):
        _id = self.initial_responses[0]['_id']
        read_response = self.mock_coll.get_response_by_id(_id)
        self.assertEqual(read_response, self.initial_responses[0])

    def test_read_all(self):
        all = self.mock_coll.get_all_responses()
        self.assertEqual(all, self.initial_responses)

    def test_read_all_by_form(self):
        res = self.mock_coll.get_responses_to_form(str(self.form_id_in_db))
        self.assertEqual(res, [r for r in self.initial_responses if r['_form'] == self.form_id_in_db])

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
        nonexisting_id = str(self.form_id_not_in_db)
        with self.assertRaises(ValueError):
            self.mock_coll.get_response_by_id(nonexisting_id)
        with self.assertRaises(ValueError):
            self.mock_coll.update_one_response(nonexisting_id, {})
        with self.assertRaises(ValueError):
            self.mock_coll.delete_response_by_id(nonexisting_id)
