from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    # this setup method runs before every test while inheriting from the BaseTest super class so it doesn't override it
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as c:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = c.post('/auth', data=json.dumps({
                    'username': 'test',
                    'password': '1234'
                }), headers={'Content-Type': 'application/json'})
                self.auth_header = f"JWT {json.loads(auth_request.data)['access_token']}"
                # this is our access token so we need to include it in the authorisation header of our GET request
                # ... that is going to get the item from the db via the API
                # the header must take this format by default with FlaskJWT

    def test_item_no_auth(self):
        with self.app() as c:
            r = c.get('/item/test')
            self.assertEqual(r.status_code, 401)

    def test_item_not_found(self):
        with self.app() as c:
            r = c.get('/item/test', headers={'Authorization': self.auth_header})
            self.assertEqual(r.status_code, 404)

    def test_item_found(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                r = c.get('/item/test', headers={'Authorization': self.auth_header})

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(r.data))

    def test_delete_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                r = c.delete('/item/test')

                self.assertEqual(r.status_code, 200)
                self.assertDictEqual(d1={'message': 'Item deleted'},
                                     d2=json.loads(r.data))

    def test_create_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                r = c.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(r.status_code, 201)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(r.data))

    def test_create_duplicate_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                c.post('/item/test', data={'price': 17.99, 'store_id': 1})
                r = c.post('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(r.status_code, 400)

    def test_put_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                r = c.put('/item/test', data={'price': 17.99, 'store_id': 1})

                self.assertEqual(r.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)
                self.assertDictEqual(d1={'name': 'test', 'price': 17.99},
                                     d2=json.loads(r.data))

    def test_put_update_item(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                c.put('/item/test', data={'price': 17.99, 'store_id': 1})
                self.assertEqual(ItemModel.find_by_name('test').price, 17.99)

                r = c.put('/item/test', data={'price': 18.99, 'store_id': 1})

                self.assertEqual(r.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('test').price, 18.99)

    def test_item_list(self):
        with self.app() as c:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 17.99, 1).save_to_db()
                r = c.get('/items')

                self.assertDictEqual(d1={'items': [{'name': 'test', 'price': 17.99}]},
                                     d2=json.loads(r.data))