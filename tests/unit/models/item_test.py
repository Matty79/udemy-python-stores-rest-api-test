from tests.unit.unit_base_test import UnitBaseTest
from models.item import ItemModel

# when these tests are first run, they won't pass as StoreModel is undefined
# you can use from models.store import StoreModel but this leaves an unused import
# you can also import BaseTest and use it in place of TestCase as a sub class but this slows tests down due to db activity
# best thing to do is import app and move it to a separate unit_base_test

class ItemTest(UnitBaseTest):
    def test_create_item(self):
        item = ItemModel('test', 19.99, 1)

        self.assertEqual(item.name, 'test',
                         "The name of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.price, 19.99,
                         "The price of the item after creation does not equal the constructor argument.")
        self.assertEqual(item.store_id, 1)
        self.assertIsNone(item.store)
        # the last two assertions check that the store ID is set correctly and that the store is none

    def test_item_json(self):
        item = ItemModel('test', 19.99, 1)
        expected = {
            'name': 'test',
            'price': 19.99
        }

        self.assertEqual(
            item.json(),
            expected,
            "The JSON export of the item is incorrect. Received {}, expected {}.".format(item.json(), expected))
