from flask_restful import Api

from app.api.resources.film import FilmsList, FilmDetail
from app.api.resources.genre import GenresList
from app.api.resources.country import CountryList
from app.api.resources.person import PersonInfo

api = Api(prefix='/api')

api.add_resource(FilmsList, '/films')
api.add_resource(FilmDetail, '/films/<int:film_id>')

api.add_resource(GenresList, '/genres')

api.add_resource(CountryList, '/countries')

api.add_resource(PersonInfo, '/person/<int:person_id>')
