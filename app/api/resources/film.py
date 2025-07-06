from flask import request
from flask_restful import Resource
from sqlalchemy.exc import NoResultFound

from app.config import get_config_value

from app.api.filter import FilmFilter
from app.models import db
from app.schemas import film_schema, detailed_film_schema

from app.utils import safe_cast
from app.api.utils import ApiResponse


class FilmsList(Resource):
	def get(self):
		args = request.args

		f_filter = FilmFilter(args)

		page = safe_cast(args.get('page'), int, 1)
		count = safe_cast(args.get('count'), int, get_config_value("PAGINATION_DEFAULT", 20))

		stmt = f_filter.query
		pagination = db.paginate(stmt, page=page, per_page=count)
		meta = {"records": pagination.total, "pages": pagination.pages}

		response = film_schema.dump(pagination.items, many=True)

		api_response = ApiResponse(data=response, meta=meta)

		return api_response.to_response()


class FilmDetail(Resource):
	def get(self, film_id):
		response = ApiResponse()
		film_id = safe_cast(film_id, int, -1)

		if film_id and film_id > 0:
			try:
				query_stmt = FilmFilter({"film_id": film_id}).query
				film = db.session.execute(query_stmt).one()[0]
				response.data = detailed_film_schema.dump(film)
			except NoResultFound:
				response.err_code = 404
		else:
			response.err_code = 404
		return response.to_response()
