from app.league.exceptions import InvalidRatingSchemeException, LeagueNotFoundException
import tinyid
from google.appengine.ext import ndb
from app.models import BaseModel


class LeagueModel(BaseModel):
    KEY_NAME_FIELDS = ['user_id', 'league_id']

    league_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty()
    scheme_choices = ['ELO', 'type1', 'type2']
    rating_scheme = ndb.StringProperty(required=True, choices=scheme_choices)
    description = ndb.TextProperty(indexed=False)
    participant_count = ndb.IntegerProperty(default=0)

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

    def update_participant_count(self, size):
        self.participant_count = size + self.participant_count
        self.put()


def create_league(user, name, rating_scheme, description=None):
    if rating_scheme not in LeagueModel.rating_scheme._choices:
        raise InvalidRatingSchemeException("Invalid rating scheme %s" % rating_scheme)
    league_id = LeagueModel.generate_id()
    key = LeagueModel.build_key(league_id, user.key)
    new_league = LeagueModel(key=key, league_id=league_id, name=name, rating_scheme=rating_scheme,
                             description=description)
    new_league.put()

    return new_league


def update_league(user, league_id, name, rating_scheme, description=None):
    if not league_id:
        raise ValueError('league_id is required')

    key = LeagueModel.build_key(league_id, user.key)
    league = key.get()
    
    if not league:
        raise LeagueNotFoundException("There is no league for league_id %s" % league_id)
    if rating_scheme not in LeagueModel.rating_scheme._choices:
        raise InvalidRatingSchemeException("Invalid rating scheme %s" % rating_scheme)

    league.name = name
    league.rating_scheme = rating_scheme
    league.description = description
    league.put()

    return league


def delete_league(user, league_id):
    key = LeagueModel.build_key(league_id, user.key)
    if key.get() is None:
        raise LeagueNotFoundException()
    else:
        return key.delete()