from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:  # this client can do POST requests, for example
            with self.app_context():  # this allows full app functionality, e.g. save to db etc.
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                # this is effectively testing our API as if we were an external user
                # data being sent is a dictionary that is not being converted to JSON data on the fly, it's form data
                # by default the parser looks for a field in the form section, then JSON and so on for valid data types

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully'}, json.loads(response.data))
                # the response.data is a dictionary that gets converted into JSON when the request is sent
                # so we convert it back to a Python dictionary with json.loads, allowing the comparison

    def test_register_and_login(self):
        with self.app() as client:  # this client can do POST requests, for example
            with self.app_context():  # this allows us to save to db etc.
                client.post('/register', data={'username': 'test', 'password': '1234'})
                auth_response = client.post('/auth',
                                            data=json.dumps({'username': 'test', 'password': '1234'}),
                                            headers={'Content-Type': 'application/json'})
                # /auth needs JSON so json.dumps takes a dictionary and dumps a string
                # json.dump needs a file pointer to save your dictionary into a file
                # header tells the web server that content type is JSON

                self.assertIn('access_token', json.loads(auth_response.data).keys())
                # converts request data into a JSON and gets its keys so we are checking for ['access_token'] string
                # appears within the list

    def test_register_duplicate_user(self):
        with self.app() as client:  # this client can do POST requests, for example
            with self.app_context():  # this allows us to save to db etc.
                client.post('/register', data={'username': 'test', 'password': '1234'})
                response = client.post('/register', data={'username': 'test', 'password': '1234'})
                # first post request saves the user, second one should generate 400 error due to duplication

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'}, json.loads(response.data))