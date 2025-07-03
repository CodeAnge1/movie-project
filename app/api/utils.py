from flask import jsonify


class ApiResponse:
	def __init__(self, err_code=200, data=None, meta=None):
		self.data = data if data is data else {}
		self.meta = meta if meta else {}
		self.err_code = err_code

	def to_dict(self):
		result = {
			"data": self.data,
			"meta": self.meta
		}
		return result

	def to_response(self):
		response = jsonify(self.to_dict())
		response.status = self.err_code

		return response
