from flask import render_template

from app.main import bp


@bp.route('/')
@bp.route('/home')
def home():
	return render_template("main.html")


@bp.route('/search')
def search():
	return render_template("search.html")


@bp.route('/film/<int:film_id>')
def film(film_id):
	return render_template("info.html")
