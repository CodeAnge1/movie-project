def safe_cast(value, new_type, default=None):
	try:
		return new_type(value) if value else default
	except (TypeError, ValueError):
		return default
