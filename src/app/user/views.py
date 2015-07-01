from functools import wraps
from google.appengine.api import users
from flask import Blueprint, redirect, request, g, url_for, render_template
from .forms import SettingsForm
from .models import update_user, User, create_user

user = Blueprint('user', __name__, url_prefix='/user')


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
        existing_user = User.build_key(user_id=user_id).get()
        if not existing_user:
            existing_user = create_user(user_id)
        return existing_user

    return None


@user.route('/settings/', methods=['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm(request.form, obj=g.user)
    if request.method == 'POST' and form.validate():
        update_user(g.user.user_id, form.name.data, form.company_name.data)
        return redirect(url_for('user.settings'))

    return render_template('user/settings.html', form=form, **g.context)


@user.route('/dashboard/')
@login_required
def user_dashboard():
    if not g.is_logged_in:
        return redirect(g.auth_url)

    return render_template("user/dashboard.html", **g.context)