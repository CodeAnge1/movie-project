from flask_marshmallow import Marshmallow

ma = Marshmallow()

from .model_schemas import *

film_schema = FilmSchema()
detailed_film_schema = FilmDetailedSchema()
genre_schema = GenreSchema()
country_schema = CountrySchema()
person_schema = PersonSchema()
film_person_schema = FilmPersonSchema()
media_schema = MediaSchema()
trailer_schema = TrailerSchema()
