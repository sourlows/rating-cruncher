from google.appengine.ext import ndb
from models import BaseModel


class User(BaseModel):

    KEY_NAME_FIELDS = ['user_id']

    user_id = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(indexed=False)
    last_name = ndb.StringProperty(indexed=False)


def create_user(user_id, first_name=None, last_name=None):
    if not user_id:
        raise ValueError('user_id is required')

    key = User.build_key(user_id=user_id)
    new_user = User(key=key, user_id=user_id, first_name=first_name, last_name=last_name)
    new_user.put()

    return new_user


def update_user(user_id, first_name=None, last_name=None):
    if not user_id:
        raise ValueError('user_id is required')
    key = User.build_key(user_id=user_id)
    existing_user = key.get()
    if not existing_user:
        raise ValueError("There is no user for user_id %s" % user_id)
    existing_user.first_name = first_name
    existing_user.last_name = last_name
    existing_user.put()
    return