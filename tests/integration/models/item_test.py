from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            StoreModel('test').save_to_db()
            item = ItemModel('test', 19.99, 1)
# this is the same test as section 5 but we add the store_id integer 1 to the parameters
# SQLLite, which we are using per base_test does not enforce foreign key constraints
# so this test will pass even though we haven't created a store
# if we were to switch to postgreSQL for example in base_test, the test would fail
# adding a StoreModel as we have done above will cause the test to pass with a postgreSQL db

            self.assertIsNone(ItemModel.find_by_name('test'),
                              "Found an item with name {}, but expected not to.".format(item.name))

            item.save_to_db()

            self.assertIsNotNone(ItemModel.find_by_name('test'))

            item.delete_from_db()

            self.assertIsNone(ItemModel.find_by_name('test'))

    def test_store_relationship(self):
        with self.app_context():
            store = StoreModel('test_store')
            item = ItemModel('test', 19.99, 1)

            store.save_to_db()
            item.save_to_db()

            self.assertEqual(item.store.name, 'test_store')
# the store property of the item is itself a StoreModel object so we have access to the name property