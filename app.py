import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT, JWTError
# JWT Error happens when a JWT cannot be found in the header

from security import authenticate, identity
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'matt123'
# used to encode cookies - we're not going to use this, but it's good habit to create one
api = Api(app)

jwt = JWT(app, authenticate, identity)
# this object takes in 3 functions and links them all up to allow us to call the /auth endpoint

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')


@app.errorhandler(JWTError)
def auth_error_handler(err):
    return jsonify({'message': 'Could not authorise - did you include a valid authorisation header?'}), 401
# jsonify needs to be imported to we can ensure the message can be sent back


if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
