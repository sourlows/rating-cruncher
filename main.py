"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, g, request, render_template, redirect, url_for
from google.appengine.api import users
from forms.league_form import LeagueForm
from forms.settings_form import SettingsForm
from models.league import create_league, League, update_league
from models.user import User, create_user, update_user

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
    return render_template("public.html", **g.context)


@app.route('/dashboard')
def user_dashboard():
    if not g.is_logged_in:
        return redirect(g.auth_url)

    return render_template("dashboard.html", **g.context)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not g.is_logged_in:
        return redirect(g.auth_url)

    form = SettingsForm(request.form, obj=g.user)
    if request.method == 'POST' and form.validate():
        update_user(g.user.user_id, form.name.data, form.company_name.data)
        return redirect(url_for('settings'))

    return render_template('settings.html', form=form, **g.context)


@app.route('/leagues/')
def display_leagues():
    if not g.is_logged_in:
        return redirect(g.auth_url)

    leagues = League.query(ancestor=g.user.key).fetch()
    return render_template('leagues.html', leagues=leagues, **g.context)


@app.route('/leagues/create', methods=['GET', 'POST'])
def create_league_form():
    if not g.is_logged_in:
        return redirect(g.auth_url)

    form = LeagueForm(request.form)
    if request.method == 'POST' and form.validate():
        create_league(g.user, form.name.data, form.rating_scheme.data, form.description.data)
        return redirect(url_for('display_leagues'))

    return render_template('create_league.html', form=form, **g.context)


@app.route('/leagues/edit/<string:league_id>', methods=['GET', 'POST'])
def edit_league_form(league_id):
    if not g.is_logged_in:
        return redirect(g.auth_url)

    form = LeagueForm(request.form)
    if request.method == 'POST' and form.validate():
        update_league(g.user, league_id, form.name.data, form.rating_scheme.data, form.description.data)
        return redirect(url_for('display_leagues'))

    key = League.build_key(league_id, g.user.key)
    league = key.get()
    form = LeagueForm(obj=league)

    return render_template('edit_league.html', form=form, league=league, **g.context)



@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
