from flask_restful import Resource

from app.api.utils import ApiResponse

from app.models import Genre
from app.schemas import genre_schema


class GenresList(Resource):
	def get(self):
		response = genre_schema.dump(Genre.query.all(), many=True)
		return ApiResponse(data=response).to_response()
