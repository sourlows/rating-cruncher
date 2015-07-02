from .base import api_module, api_auth
from flask import jsonify


@api_module.route('/league/')
@api_auth.login_required
def get_all_leagues():
    """Return all leagues associated with a user."""
    return jsonify({'stuff': 'a value'})