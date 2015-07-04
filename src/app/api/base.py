from flask import jsonify, make_response, Blueprint
from flask.ext.httpauth.flask_httpauth import HTTPBasicAuth
from app.user.models import UserModel

api_auth = HTTPBasicAuth()
api_module = Blueprint('api', __name__, url_prefix='/api')


@api_auth.get_password
def get_pw(username):
    user = UserModel.build_key(user_id=username).get()
    if user:
        return user.api_key
    return None


@api_auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)