import os

from pathlib import Path
from dotenv import load_dotenv

from flask import current_app

basedir = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(basedir, '.env'))


def get_config_value(var_name, default=None):
	return current_app.config.get(var_name, default)


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
	PAGINATION_DEFAULT = 20
	POSTER_IMAGE_BASE_URL = os.getenv("POSTER_IMAGE_BASE_URL", "https://avatars.mds.yandex.net/get-kinopoisk-image/")
	PERSON_PHOTO_BASE_URL = os.getenv("PERSON_PHOTO_BASE_URL", "https://st.kp.yandex.net/images/actor_iphone/iphone")
	YT_TRAILER_BASE_URL = os.getenv("YT_TRAILER_BASE_URL", "https://www.youtube.com/embed/")
	KP_BASE_URL = os.getenv("KP_BASE_URL", "https://www.kinopoisk.ru/film/")


class ProductionConfig(BaseConfig):
	pass


class DevConfig(BaseConfig):
	DEBUG = True
	JSON_SORT_KEYS = False
	JSON_AS_ASCII = False
