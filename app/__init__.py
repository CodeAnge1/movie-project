from flask import Flask

from app.api import api
from app.config import *
from app.models import db
from app.schemas import ma

from app.main import bp as main_bp


def create_app():
	app = Flask(__name__)
	choice_config_obj(app)

	api.init_app(app)
	db.init_app(app)
	ma.init_app(app)

	app.register_blueprint(main_bp)

	return app
