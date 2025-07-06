from marshmallow import fields

from app.schemas import ma
from app.config import get_config_value
from app.models import Film, Genre, Country, Person, FilmPerson, Media, Trailer


class GenreSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Genre


class CountrySchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Country


class PersonSchema(ma.SQLAlchemyAutoSchema):
	full_url = fields.Method("get_full_photo_url")

	class Meta:
		model = Person
		exclude = ("photo_url",)

	def get_full_photo_url(self, obj):
		return get_config_value("PERSON_PHOTO_BASE_URL", "") + obj.photo_url if obj.photo_url else ""


class FilmPersonSchema(ma.SQLAlchemyAutoSchema):
	person = fields.Nested(PersonSchema, exclude=("id",))

	class Meta:
		model = FilmPerson
		include_fk = True


class MediaSchema(ma.SQLAlchemyAutoSchema):
	full_url = fields.Method("get_full_img_url")

	class Meta:
		model = Media
		exclude = ("url",)

	def get_full_img_url(self, obj):
		return get_config_value("POSTER_IMAGE_BASE_URL", "") + obj.url if obj.url else ""


class TrailerSchema(ma.SQLAlchemyAutoSchema):
	full_url = fields.Method("get_full_trailer_url")

	class Meta:
		model = Trailer
		exclude = ("url",)

	def get_full_trailer_url(self, obj):
		return get_config_value("YT_TRAILER_BASE_URL", "") + obj.url if obj.url else ""


class FilmSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Film
		include_fk = True

	genres = fields.List(fields.Nested(GenreSchema(only=("name",))))
	countries = fields.List(fields.Nested(CountrySchema(only=("name",))))
	media = fields.List(fields.Nested(MediaSchema(exclude=("id",))))


class FilmDetailedSchema(FilmSchema):
	class Meta:
		model = Film
		include_fk = True

	film_people = fields.List(fields.Nested(FilmPersonSchema(exclude=("id", "position"))))
	trailers = fields.List(fields.Nested(TrailerSchema()))
