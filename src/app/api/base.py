from google.appengine.datastore import datastore_query
from flask import jsonify, make_response, Blueprint
from flask_httpauth.flask_httpauth import HTTPBasicAuth
from app.user.models import UserModel
from flask_restful import Resource, reqparse

API_AUTH = HTTPBasicAuth()
API_MODULE = Blueprint('api', __name__, url_prefix='/api')


@API_AUTH.get_password
def get_pw(username):
    user = UserModel.build_key(user_id=username).get()
    if user:
        return user.api_key
    return None


@API_AUTH.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


class AbstractApiArgument(object):
    DEFAULTS = {
        'type': str,
        'required': False,
        'location': 'json'
    }

    def __init__(self, name, **kwargs):
        self.properties = {}
        self.properties.update(self.DEFAULTS)
        self.properties.update(kwargs)
        self.name = name


class StringArgument(AbstractApiArgument):
    def __init__(self, name, **kwargs):
        super(StringArgument, self).__init__(name, type=str, **kwargs)


class IntegerArgument(AbstractApiArgument):
    def __init__(self, name, **kwargs):
        super(IntegerArgument, self).__init__(name, type=int, **kwargs)


class FloatArgument(AbstractApiArgument):
    def __init__(self, name, **kwargs):
        super(FloatArgument, self).__init__(name, type=float, **kwargs)


class DatastoreCursorArgument(AbstractApiArgument):
    def __init__(self, name, **kwargs):
        super(DatastoreCursorArgument, self).__init__(name, type=datastore_query.Cursor, **kwargs)


class BaseAuthResource(Resource):
    """
    All resources which require authentication should extend this class.
    REQUIRED_ARGS defines a set of argument names which are required for this resource to return any response.
    OPTIONAL_ARGS defines a set of argument names which are optional for this resource.
    self.user is the user object corresponding to the request's api user, it is available to all inheritors
    """
    decorators = [API_AUTH.login_required]

    API_USER = 'username'

    ARGUMENTS = frozenset([])

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        for argument in self.ARGUMENTS:
            self.reqparse.add_argument(argument.name, **argument.properties)

        # get username
        self.reqparse.add_argument('username', type=str, required=True, location='authorization')

        self.args = self.reqparse.parse_args()
        self.user = UserModel.build_key(user_id=self.args[self.API_USER]).get()
        super(BaseAuthResource, self).__init__()
