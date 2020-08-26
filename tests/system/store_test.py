from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

# as a rule of thumb, you should have as few system tests as possible
# you should have more integration tests than systems tests
# you should have more unit tests than integration tests
# mocking can be used to run integration and unit tests in your resources though we've not done this

class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual({'name': 'test', 'items': []}, json.loads(response.data))

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')
                response = client.post('/store/test')

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': "A store with name 'test' already exists."}, json.loads(response.data))

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test')  # alternatively you could use StoreModel('test').save_to_db()
                response = client.delete('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'}, json.loads(response.data))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertEqual({'name': 'test', 'items': []}, json.loads(response.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'}, json.loads(response.data))
                # the second test not as useful as status code check as client won't check response if 404

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                response = client.get('/store/test')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]},
                                     json.loads(response.data))

    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()

                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': []}]}, json.loads(response.data))

    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 19.99, 1).save_to_db()

                response = client.get('/stores')
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual({'stores': [{'name': 'test', 'items': [{'name': 'test', 'price': 19.99}]}]},
                                     json.loads(response.data))
                # horrible brackets!
