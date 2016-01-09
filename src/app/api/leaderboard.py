from app.api.base import BaseAuthResource, StringArgument, IntegerArgument, DatastoreCursorArgument
from app.participant.models import ParticipantModel
from flask_restful import fields, marshal

LEADERBOARD_TEMPLATE = {
    'name': fields.String,
    'rating': fields.Float,
    'games_played': fields.Integer,
    'wins': fields.Integer,
    'losses': fields.Integer,
    'ties': fields.Integer,
    'k_factor': fields.Integer,
}

SORT_ASCENDING = 'ascending'
SORT_DESCENDING = 'descending'
SORT_OPTIONS = ['name', 'rating', 'games_played', 'k_factor', 'wins', 'losses', 'ties']


class LeaderboardAPI(BaseAuthResource):
    ARGUMENTS = frozenset([
        StringArgument('sort_direction'),
        StringArgument('sort_by'),
        IntegerArgument('page_size'),
        DatastoreCursorArgument('cursor'),
    ])

    def get(self, league_id):
        """ Return a sorted leaderboard representing participants in a league """
        sort_by = self.args.get('sort_by')
        sort_direction = self.args.get('sort_direction')
        cursor = self.args.get('cursor')
        page_size = self.args.get('page_size')

        if sort_by and hasattr(ParticipantModel, sort_by) and sort_by in SORT_OPTIONS:
            sort_by = getattr(ParticipantModel, sort_by)
        elif sort_by is None:
            sort_by = getattr(ParticipantModel, 'rating')
        else:
            return 'Invalid sort_by option %s' % sort_by, 400

        if sort_direction == SORT_DESCENDING or not sort_direction:
            leaderboard = ParticipantModel.query(getattr(ParticipantModel, 'league_id') == league_id).order(-sort_by)
        elif sort_direction == SORT_ASCENDING:
            leaderboard = ParticipantModel.query(getattr(ParticipantModel, 'league_id') == league_id).order(sort_by)
        else:
            return 'Invalid sort direction %s' % sort_direction, 400

        results, cursor, more = leaderboard.fetch_page(page_size=page_size, start_cursor=cursor)

        return {
            'leaderboard': [marshal(l, LEADERBOARD_TEMPLATE) for l in results],
            'cursor': cursor
        }
