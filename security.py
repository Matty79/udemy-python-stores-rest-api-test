from werkzeug.security import safe_str_cmp
# this library compares strings
from models.user import UserModel


def authenticate(username, password):
    """
    Function gets called when a user calls the /auth endpoint
    with their username and password
    FlaskJWT implements the endpoint itself but we still have to define what happens when we receive user / pass
    :param username: User's username in string format
    :param password: User's unencrypted password in string format
    :return: a UserModel object if authentication was successful, none otherwise
    """

    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

    # we don't have to include return None (if username / pass don't match)
    # in the above function as it is the default in Python

def identity(payload):
    """
    Function that gets called when user has already authenticated, and Flask-JWT
    verified their authorisation header is correct
    :param payload: A dictionary with 'identity' key, which is the user id
    :return: A UserModel object
    """
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)