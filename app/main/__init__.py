from flask import Blueprint

bp = Blueprint('main', __name__, template_folder='../../frontend/templates')
print(bp.template_folder)

from app.main import routes
