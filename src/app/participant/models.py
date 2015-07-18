from app.models import BaseModel
from google.appengine.ext import ndb

import tinyid
from app.league.models import LeagueModel
from app.user.models import UserModel

__author__ = 'Alex'


class ParticipantModel(BaseModel):
    participant_id = ndb.StringProperty(required=True)
    league_id = ndb.StringProperty(required=True)
    user_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty(indexed=False)
    rating = ndb.FloatProperty()

    @classmethod
    def generate_id(cls):
        """ Generate a unique id. """
        if ndb.in_transaction():
            tiny_id = tinyid.TinyIDGenerator(namespace='P').generate_tinyid(run_in_transaction=False).upper()
        else:
            tiny_id = tinyid.TinyIDGenerator(namespace='P').generate_tinyid(run_in_transaction=True).upper()
        return '%s-%s' % ('P', tiny_id)

    @classmethod
    def build_key(cls, participant_id):
        """ Builds a key in the default namespace. """
        key = ndb.model.Key(cls.__name__, participant_id)
        return key

    @classmethod
    def _post_delete_hook(cls, key, future):
        participant = key.get()
        user_key = UserModel.build_key(cls.user_id)
        league_key = LeagueModel.build_key(participant.league_id, user_key)
        league = league_key.get()
        league.update_participant_count(-1)

    def _post_put_hook(self):
        user_key = UserModel.build_key(self.user_id)
        league_key = LeagueModel.build_key(self.league_id, user_key)
        league = league_key.get()
        league.update_participant_count(1)


def create_participant(user_id, league_id, name, rating=1400.0):
    participant_id = ParticipantModel.generate_id()
    key = ParticipantModel.build_key(participant_id)
    new_participant = ParticipantModel(key=key, participant_id=participant_id, league_id=league_id,
                                       user_id=user_id, name=name, rating=rating)
    new_participant.put()
    return new_participant


def delete_participant(participant_id):
    key = ParticipantModel.build_key(participant_id)
    return key.delete()