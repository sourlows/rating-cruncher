from models import BaseModel
from google.appengine.ext import ndb
import tinyid


class League(BaseModel):
    KEY_NAME_FIELDS = ['user_id', 'league_id']

    league_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    rating_scheme = ndb.StringProperty()
    description = ndb.TextProperty(indexed=False)

    @classmethod
    def generate_id(cls):
        """ Generate a unique id. """
        if ndb.in_transaction():
            tiny_id = tinyid.TinyIDGenerator(namespace='LG').generate_tinyid(run_in_transaction=False).upper()
        else:
            tiny_id = tinyid.TinyIDGenerator(namespace='LG').generate_tinyid(run_in_transaction=True).upper()
        return '%s-%s' % ('LG', tiny_id)

    @classmethod
    def build_key(cls, league_id, user_key):
        """ Builds a key in the default namespace. """
        key = ndb.model.Key(cls.__name__, league_id, parent=user_key)
        return key


def create_league(user, name, rating_scheme, description=None):
    league_id = League.generate_id()
    key = League.build_key(league_id, user.key)
    new_league = League(key=key, league_id=league_id, name=name, rating_scheme=rating_scheme,
                        description=description)
    new_league.put()

    return new_league


def update_league(user, league_id, name, rating_scheme, description=None):
    if not league_id:
        raise ValueError('league_id is required')

    key = League.build_key(league_id, user.key)
    league = key.get()
    if not league:
        raise ValueError("There is no league for league_id %s" % league_id)

    league.name = name
    league.rating_scheme = rating_scheme
    league.description = description
    league.put()
    return