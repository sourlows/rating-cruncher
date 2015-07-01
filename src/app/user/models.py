from google.appengine.ext import ndb
from app.models import BaseModel


class User(BaseModel):

    KEY_NAME_FIELDS = ['user_id']

    user_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty(indexed=False)
    company_name = ndb.StringProperty()


def create_user(user_id, name=None, company_name=None):
    if not user_id:
        raise ValueError('user_id is required')

    key = User.build_key(user_id=user_id)
    new_user = User(key=key, user_id=user_id, name=name, company_name=company_name)
    new_user.put()

    return new_user


def update_user(user_id, name=None, company_name=None):
    if not user_id:
        raise ValueError('user_id is required')

    key = User.build_key(user_id=user_id)
    existing_user = key.get()
    if not existing_user:
        raise ValueError("There is no user for user_id %s" % user_id)

    existing_user.name = name
    existing_user.company_name = company_name
    existing_user.put()
    return