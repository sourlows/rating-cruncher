from app.participant.forms import ParticipantsForm
from app.participant.models import create_participant
from app.user.views import login_required
from flask import Blueprint, redirect, request, g, url_for, render_template

__author__ = 'Alex'

participant_module = Blueprint('participant', __name__, url_prefix='/league/participant')


@participant_module.route('/create/', methods=['GET', 'POST'])
@login_required
def create_participant(league_id):
    if not g.is_logged_in:
        return redirect(g.auth_url)

    form = ParticipantsForm(request.form)
    if request.method == 'POST' and form.validate():
        create_participant(g.user_id, league_id, form.name)
        return redirect(url_for('participant.create_participant'))

    return render_template('participant/create_participant.html', form=form, **g.context)
