from flask import Blueprint, render_template
from flask_login import login_required, current_user

book = Blueprint('book', __name__)