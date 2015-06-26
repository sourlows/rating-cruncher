"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, g
from flask import render_template
from google.appengine.api import users
from models.user import User, create_user

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
@app.before_request
def before_request(*args, **kwargs):
    g.user = get_user()
    g.is_logged_in = bool(g.user)
    g.auth_url = users.create_logout_url('/') if g.is_logged_in else users.create_login_url('/dashboard')
    g.context = {
        'auth_url': g.auth_url,
        'is_logged_in': g.is_logged_in,
    }


def get_user():
    session_user = users.get_current_user()
    if session_user:
        user_id = session_user.user_id()
        existing_user = User.build_key(user_id=user_id).get()
        if not existing_user:
            existing_user = create_user(user_id)
        return existing_user

    return None



@app.route('/')
def index():
    """Return a friendly HTTP greeting."""
    g.context['name'] = g.user.name
    return render_template("public.html", **g.context)


@app.route('/dashboard')
def user_dashboard():
    return render_template("dashboard.html", **g.context)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
