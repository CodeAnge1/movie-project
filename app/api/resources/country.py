from flask_restful import Resource

from app.api.utils import ApiResponse

from app.models import Country
from app.schemas import country_schema


class CountryList(Resource):
	def get(self):
		response = country_schema.dump(Country.query.all(), many=True)
		return ApiResponse(data=response).to_response()
