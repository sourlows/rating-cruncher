"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask
from flask import render_template
from google.appengine.api import users
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    is_logged_in = bool(users.get_current_user())
    auth_url = users.create_logout_url('/') if is_logged_in else users.create_login_url('/')
    context = {
        'auth_url': auth_url,
        'is_logged_in': is_logged_in,
    }
    return render_template("index.html", **context)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
