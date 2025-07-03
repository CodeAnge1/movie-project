from typing import cast

from sqlalchemy import select, and_

from app.models import Film, Genre, Country
from app.utils import safe_cast


class FilmFilter:
	def __init__(self, args):
		self.args = args if args else {}
		self.query = select(Film)

		self.apply_filters()

	def apply_filters(self):
		self.one_id_filter()
		self.multiple_ids_filter()
		self.genre_filter()
		self.country_filter()
		self.type_filter()
		self.title_filter()
		self.year_filter()
		self.rating_filter()
		self.duration_filter()

	def one_id_filter(self):
		film_id = self.args.get("film_id")
		if film_id:
			self.query = self.query.where(
				cast("ColumnElement[bool]", Film.id == film_id)
			)

	def multiple_ids_filter(self):
		film_ids = self.args.get("film_ids", "").split(",")
		correct_ids = [corr_id for id in film_ids if (corr_id := safe_cast(id, int))]
		if film_ids[0]:
			self.query = self.query.where(Film.id.in_(correct_ids))

	def genre_filter(self):
		genres = self.args.get("genres", "").split(",")
		if genres[0]:
			self.query = self.query.join(Film.genres).where(Genre.name.in_(genres))

	def country_filter(self):
		countries = self.args.get("countries", "").split(",")
		if countries[0]:
			self.query = self.query.join(Film.countries).where(Country.name.in_(countries))

	def type_filter(self):
		types = self.args.get("types", "").split(",")
		if types[0]:
			self.query = self.query.where(Film.type.in_(types))

	def title_filter(self):
		title = safe_cast(self.args.get("title"), str, "%")
		original_title = safe_cast(self.args.get("original_title"), str, "%")
		self.query = self.query.where(and_(
			Film.title.like(f"%{title}%"),
			Film.original_title.like(f"%{original_title}%")
		))

	def year_filter(self):
		years = self.args.get("years", "").split(",")
		correct_years = []
		if years[0]:
			correct_years = [corr_year for year in years if (corr_year := safe_cast(year, int))]
		if correct_years:
			self.query = self.query.where(Film.year.in_(correct_years))
		else:
			year_from = safe_cast(self.args.get("year_from"), int, 1890)
			year_to = safe_cast(self.args.get("year_to"), int, 2277)
			self.query = self.query.where(Film.year.between(year_from, year_to))

	def rating_filter(self):
		rating_from = safe_cast(self.args.get("rating_from"), float, 0.0)
		rating_to = safe_cast(self.args.get("rating_to"), float, 10.0)
		self.query = self.query.where(Film.rating.between(rating_from, rating_to))

	def duration_filter(self):
		duration_from = safe_cast(self.args.get("duration_from"), int, 0)
		duration_to = safe_cast(self.args.get("duration_to"), int, 1000)
		self.query = self.query.where(Film.duration.between(duration_from, duration_to))
