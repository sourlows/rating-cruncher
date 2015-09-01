from app.models import BaseModel
from google.appengine.ext import ndb

import tinyid
from app.league.models import LeagueModel


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


def create_participant(user, league_id, name, rating=1400.0):
    participant_id = ParticipantModel.generate_id()
    key = ParticipantModel.build_key(participant_id)
    new_participant = ParticipantModel(key=key, participant_id=participant_id, league_id=league_id,
                                       user_id=user.user_id, name=name, rating=rating)
    new_participant.put()
    league = LeagueModel.build_key(league_id, user.key).get()
    league.update_participant_count(1)
    return new_participant


def update_participant(user, participant_id, league_id, name, rating):
    if not participant_id:
        raise ValueError('participant_id is required')

    participant = ParticipantModel.build_key(participant_id).get()
    if not participant:
        raise ValueError('There is no participant for participant_id %s' % participant_id)

    participant.user_id = user.user_id
    participant.name = name
    participant.league_id = league_id
    participant.rating = rating
    participant.put()

    return participant


def delete_participant(user, participant_id):
    key = ParticipantModel.build_key(participant_id)
    participant = key.get()
    if not participant:
        raise ValueError('Invalid participant id %s' % participant_id)
    league = LeagueModel.build_key(participant.league_id, user.key).get()
    league.update_participant_count(-1)
    return key.delete()