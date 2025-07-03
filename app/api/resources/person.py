from flask_restful import Resource

from app.api.utils import ApiResponse

from app.models import Person
from app.schemas import person_schema


class PersonInfo(Resource):
	def get(self, person_id):
		response = person_schema.dump(Person.query.filter_by(id=person_id).first())
		return ApiResponse(data=response).to_response()
