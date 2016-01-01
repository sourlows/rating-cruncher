from functools import wraps
from google.appengine.api import users
from app.user.forms import SettingsForm
from app.user.models import UserModel, create_user, update_user
from flask import Blueprint, redirect, request, g, url_for, render_template

USER_MODULE = Blueprint('user', __name__, url_prefix='/user')


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(g.auth_url)
        return func(*args, **kwargs)
    return decorated_view


def get_authed_user():
    session_user = users.get_current_user()
    if session_user:
        user_id = session_user.user_id()
        existing_user = UserModel.build_key(user_id=user_id).get()
        if not existing_user:
            existing_user = create_user(user_id)
        return existing_user

    return None


@USER_MODULE.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm(request.form, obj=g.user)
    if request.method == 'POST' and form.validate():
        update_user(g.user.user_id, form.name.data, form.company_name.data)
        return redirect(url_for('user.settings'))

    g.context['api_key'] = g.user.api_key
    return render_template('user/settings.html', form=form, **g.context)


@USER_MODULE.route('/dashboard/')
@login_required
def user_dashboard():
    if not g.is_logged_in:
        return redirect(g.auth_url)

    return render_template("user/dashboard.html", **g.context)
