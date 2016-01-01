from app.models import BaseModel
from app.league.models import LeagueModel
from google.appengine.ext import ndb

import tinyid

class ParticipantModel(BaseModel):
    participant_id = ndb.StringProperty(required=True)
    league_id = ndb.StringProperty(required=True)
    user_id = ndb.StringProperty(required=True)
    name = ndb.StringProperty(indexed=False)
    rating = ndb.FloatProperty()

    # set from League based on games_played; initially league.k_factor_initial
    # if games_played > k_factor_scaling, set to league.k_factor_min
    k_factor = ndb.FloatProperty(required=True)
    games_played = ndb.IntegerProperty(default=0)
    wins = ndb.IntegerProperty(default=0)
    losses = ndb.IntegerProperty(default=0)
    ties = ndb.IntegerProperty(default=0)

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
        # pylint: disable=W0221
        key = ndb.model.Key(cls.__name__, participant_id)
        return key


def create_participant(user, league_id, name, rating=1400.0):
    participant_id = ParticipantModel.generate_id()
    key = ParticipantModel.build_key(participant_id)
    league = LeagueModel.build_key(league_id, user.key).get()

    new_participant = ParticipantModel(key=key, participant_id=participant_id, league_id=league_id,
                                       user_id=user.user_id, name=name, rating=rating, k_factor=league.k_factor_initial)

    if league.k_factor_scaling == 0:
        new_participant.k_factor = league.k_factor_min

    new_participant.put()
    league.update_participant_count(1)
    return new_participant


def update_participant(participant_id, name=None, rating=None):
    if not participant_id:
        raise ValueError('participant_id is required')

    participant = ParticipantModel.build_key(participant_id).get()
    if not participant:
        raise ValueError('There is no participant for participant_id %s' % participant_id)

    if name is not None:
        participant.name = name

    if rating is not None:
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
