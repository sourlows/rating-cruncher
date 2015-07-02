from flask import jsonify, make_response
from flask.ext.httpauth.flask_httpauth import HTTPBasicAuth
from ..user import User

api_auth = HTTPBasicAuth()


@api_auth.get_password
def get_pw(username):
    user = User.build_key(user_id=username).get()
    if user:
        return user.api_key
    return None


@api_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)