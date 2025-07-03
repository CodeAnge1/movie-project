from marshmallow import fields

from app.schemas import ma

from app.models import Film, Genre, Country, Person, FilmPerson, Media, Trailer


class GenreSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Genre


class CountrySchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Country


class PersonSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Person


class FilmPersonSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = FilmPerson
		include_fk = True


class MediaSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Media


class TrailerSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Trailer


class FilmSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Film
		include_fk = True

	genres = fields.List(fields.Nested(GenreSchema(only=("name",))))
	countries = fields.List(fields.Nested(CountrySchema(only=("name",))))
	film_people = fields.List(fields.Nested(FilmPersonSchema(only=("person_id", "role"))))
	media = fields.List(fields.Nested(MediaSchema(exclude=("id",))))
	trailers = fields.List(fields.Nested(TrailerSchema()))
