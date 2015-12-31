from app.league.forms import LeagueForm
from app.league.models import LeagueModel, create_league, update_league
from app.user.views import login_required
from flask import Blueprint, redirect, request, g, url_for, render_template

LEAGUE_MODULE = Blueprint('league', __name__, url_prefix='/league')


@LEAGUE_MODULE.route('/index/')
@login_required
def display_leagues():
    leagues = LeagueModel.query(ancestor=g.user.key).fetch()
    return render_template('league/leagues.html', leagues=leagues, **g.context)


@LEAGUE_MODULE.route('/create/', methods=['GET', 'POST'])
@login_required
def create_league_form():
    if not g.is_logged_in:
        return redirect(g.auth_url)

    form = LeagueForm(request.form)
    if request.method == 'POST' and form.validate():
        create_league(g.user, form.name.data, form.rating_scheme.data, form.description.data, form.k_factor_scaling)
        return redirect(url_for('league.display_leagues'))

    return render_template('league/create_league.html', form=form, **g.context)


@LEAGUE_MODULE.route('/edit/<string:league_id>/', methods=['GET', 'POST'])
@login_required
def edit_league_form(league_id):
    if not g.is_logged_in:
        return redirect(g.auth_url)

    form = LeagueForm(request.form)
    if request.method == 'POST' and form.validate():
        update_league(g.user, league_id, form.name.data, form.rating_scheme.data, form.description.data)
        return redirect(url_for('league.display_leagues'))

    key = LeagueModel.build_key(league_id, g.user.key)
    league = key.get()
    form = LeagueForm(obj=league)

    return render_template('league/edit_league.html', form=form, league=league, **g.context)
