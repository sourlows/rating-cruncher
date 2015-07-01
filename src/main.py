"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from functools import wraps
from flask import Flask, g, render_template, redirect
from google.appengine.api import users
from app.user.views import get_authed_user, user_module
from app.league.views import league_module

app = Flask(__name__)
app.register_blueprint(user_module)
app.register_blueprint(league_module)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(g.auth_url)
        return func(*args, **kwargs)
    return decorated_view


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
