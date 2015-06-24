from google.appengine.ext import ndb
from models import BaseModel


class User(BaseModel):

    KEY_NAME_FIELDS = ['user_id']

    user_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty(indexed=False)


def create_user(user_id, name=None):
    if not user_id:
        raise ValueError('user_id is required')

    key = User.build_key(user_id=user_id)
    new_user = User(key=key, user_id=user_id, name=name)
    new_user.put()

    return new_user