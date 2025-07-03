import os

from pathlib import Path
from dotenv import load_dotenv

basedir = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(basedir, '.env'))


def choice_config_obj(app):
	if os.environ.get("TESTING") in ["True", "true", 1]:
		app.config.from_object(DevConfig)
	else:
		app.config.from_object(ProductionConfig)
	app.template_folder = app.config["TEMPLATE_FOLDER"]
	app.static_folder = app.config["STATIC_FOLDER"]


class BaseConfig:
	DEBUG = False
	TESTING = False
	SECRET_KEY = os.environ.get("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
	TEMPLATE_FOLDER = os.path.join(basedir, "frontend", "templates")
	STATIC_FOLDER = os.path.join(basedir, "frontend", "static")


class ProductionConfig(BaseConfig):
	pass


class DevConfig(BaseConfig):
	DEBUG = True
	JSON_SORT_KEYS = False
	JSON_AS_ASCII = False
