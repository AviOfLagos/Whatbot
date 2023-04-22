from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from models import db, Group, Member
from utils import get_group_data

group_details_bp = Blueprint('group_details_bp', __name__)

@group_details_bp.route('/group/<int:group_id>')
def get_group_details(group_id):
    group = Group.query.filter_by(id=group_id).first()
    if not group:
        abort(404)

    group_data = get_group_data(group)

    return render_template('group_details.html', group_data=group_data)