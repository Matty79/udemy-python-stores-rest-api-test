"""
BaseTest

This class should be the parent class to each non-unit test.
It allows for instantiation of the database dynamically
and makes sure that it is a new, blank database each time.
"""

from unittest import TestCase
from app import app
from db import db


class BaseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'
        app.config['DEBUG'] = False
        app.config['PROPAGATE_EXCEPTIONS'] = True
        with app.app_context():
            db.init_app(app)
# if we call db.init_app(app) after we have already made a request to our app, Flask objects even though it's not
# ...technically an issue so we need to set DEBUG to be False in the BaseTest class (it can remain True in the app)
# as setting DEBUG to False also sets PROPAGATE_EXCEPTIONS to False we need to set them to True for Flask
# what this does is that when an exception happens in the code, it is caught by the Flask error handlers
# such that any unhandled exceptions don't give clients information about your system
# if we set DEBUG to False in the app itself, we lose JWTError handling and just get 500 errors

# the setUpClass method runs once for every test class, whereas the SetUp method below runs once for every test method
    def setUp(self):
        # Make sure database exists
        with app.app_context():
            db.create_all()
        # Get a test client
        self.app = app.test_client
        # we remove brackets from app.test_client() so that we create a new test_client every time we call self.app
        self.app_context = app.app_context

    def tearDown(self):
        # Database is blank
        with app.app_context():
            db.session.remove()
            db.drop_all()

# if we weren't saving data and deleting it every test, we could move db.create_all() to the setUpClass
# and db.drop_all() to a new tearDownClass, which would look similar to the setUpClass
