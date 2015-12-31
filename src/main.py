"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from google.appengine.api import users

from app.api.participant import ParticipantAPI, ParticipantListAPI
from flask import Flask, g, render_template
from app.user.views import get_authed_user, USER_MODULE
from app.league.views import LEAGUE_MODULE
from app.api.base import API_MODULE
from flask.ext.restful import Api
from app.api.league import LeagueListAPI, LeagueAPI


app = Flask(__name__)
app.register_blueprint(USER_MODULE)
app.register_blueprint(LEAGUE_MODULE)

api = Api(API_MODULE)
api.add_resource(LeagueListAPI, '/league/')
api.add_resource(LeagueAPI, '/league/<string:league_id>')
api.add_resource(ParticipantListAPI, '/participant/<string:league_id>')
api.add_resource(ParticipantAPI, '/participant/<string:league_id>/<string:participant_id>')

app.register_blueprint(API_MODULE)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.before_request
def before_request(*args, **kwargs):
    g.user = get_authed_user()
    g.is_logged_in = bool(g.user)
    g.auth_url = users.create_logout_url('/') if g.is_logged_in else users.create_login_url('/user/dashboard/')
    g.context = {
        'auth_url': g.auth_url,
        'is_logged_in': g.is_logged_in,
    }


@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    return render_template("public.html", **g.context)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
