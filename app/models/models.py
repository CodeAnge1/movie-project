from sqlalchemy.inspection import inspect

from app.models import db

film_genres = db.Table(
	"film_genres",
	db.Column("film_id", db.Integer, db.ForeignKey("films.id")),
	db.Column("genre_id", db.Integer, db.ForeignKey("genres.id"))
)

film_countries = db.Table(
	"film_countries",
	db.Column("film_id", db.Integer, db.ForeignKey("films.id")),
	db.Column("country_id", db.Integer, db.ForeignKey("countries.id"))
)


class BaseModel:
	def __repr__(self):
		columns = inspect(self.__class__).columns
		res = {}
		for col in columns:
			res[col.name] = getattr(self, col.name)
		return f"<{self.__class__.__name__} {str(res)}>"


class Film(BaseModel, db.Model):
	__tablename__ = "films"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	kp_id = db.Column(db.Integer, nullable=False)
	type = db.Column(db.String(255), nullable=False)
	title = db.Column(db.String(255), nullable=False)
	original_title = db.Column(db.String(255), nullable=False)
	description = db.Column(db.Text, nullable=False)
	year = db.Column(db.Integer, nullable=False)
	rating = db.Column(db.Numeric(4, 2), nullable=True)
	duration = db.Column(db.Integer, nullable=False)

	media = db.relationship("Media", backref="film", lazy="dynamic")
	trailers = db.relationship("Trailer", backref="film", lazy="dynamic")
	film_people = db.relationship("FilmPerson", backref="film", lazy="dynamic")

	genres = db.relationship("Genre", secondary=film_genres, backref="film")
	countries = db.relationship("Country", secondary=film_countries, backref="film")


class Genre(BaseModel, db.Model):
	__tablename__ = "genres"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False, unique=True)


class Country(BaseModel, db.Model):
	__tablename__ = "countries"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False, unique=True)


class Person(BaseModel, db.Model):
	__tablename__ = "people"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	first_name = db.Column(db.String(255), nullable=False)
	last_name = db.Column(db.String(255), nullable=False)
	photo_url = db.Column(db.Text, nullable=False)


class FilmPerson(BaseModel, db.Model):
	__tablename__ = "film_people"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	film_id = db.Column(db.Integer, db.ForeignKey("films.id"))
	person_id = db.Column(db.Integer, db.ForeignKey("people.id"))
	role = db.Column(db.String(255), nullable=False)
	character_name = db.Column(db.String(255), nullable=True)
	position = db.Column(db.Integer, nullable=True)

	person = db.relationship("Person", backref="film_roles")


class Media(BaseModel, db.Model):
	__tablename__ = "media"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	film_id = db.Column(db.Integer, db.ForeignKey("films.id"), nullable=False)
	type = db.Column(db.String(255), nullable=False)
	url = db.Column(db.Text, nullable=False)


class Trailer(BaseModel, db.Model):
	__tablename__ = "trailers"

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	film_id = db.Column(db.Integer, db.ForeignKey("films.id"), nullable=False)
	url = db.Column(db.Text, nullable=False)
