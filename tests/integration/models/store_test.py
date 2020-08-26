from models.item import ItemModel
from models.store import StoreModel

from tests.base_test import BaseTest

class StoreTest(BaseTest):
    def test_create_store_items_empty(self):
        store = StoreModel('test')

        self.assertListEqual(store.items.all(), [],
                             "The store's items length was not 0 even though no items were added")

    def test_crud(self):
        with self.app_context():
            store = StoreModel('test')

            self.assertIsNone(StoreModel.find_by_name('test'),
                                                      "error message goes here")

            store.save_to_db()

            self.assertIsNotNone(StoreModel.find_by_name('test'),
                                                      "error message goes here")

            store.delete_from_db()

            self.assertIsNone(StoreModel.find_by_name('test'),
                                                      "error message goes here")

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

# store doesn't need an item but item needs a store so it's important to save the store to a db first

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(store.items.count(), 1)
# counts number of items
            self.assertEqual(store.items.first().name, 'test_item')
# gives first item returned by SQL query, which is an ItemModel object

    def test_store_json(self):
        with self.app_context():
            store = StoreModel('test')
            item = ItemModel('test_item', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            expected = {
            'name': 'test',
            'items': [{'name': 'test_item', 'price': 19.99}]
             }

            self.assertDictEqual(store.json(), expected)