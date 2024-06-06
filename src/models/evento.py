from sqlobject import SQLObject, IntCol, StringCol, FloatCol, ForeignKey, DateTimeCol
from enum import Enum


class Category(Enum):
		UFC = "UFC"
		e_Sports = "e-Sports"
		Zoera = "Zoera"
		Generica = "Genérica"
		
		@staticmethod
		def get_from_value(category_value):
				for category in Category:
						if category.value == category_value:
								return category
				return None


class Evento(SQLObject):
		title = StringCol()
		category = StringCol()
		option_a = StringCol()
		option_b = StringCol()
		total_bets_a = IntCol(default=0.0)
		total_bets_b = IntCol(default=0.0)
		total_amount_a = FloatCol(default=0.0)
		total_amount_b = FloatCol(default=0.0)
		odds_a = FloatCol(default=1.0)
		odds_b = FloatCol(default=1.0)
		user_who_started = ForeignKey('User')
		started_at = DateTimeCol(default=DateTimeCol.now)
		status = StringCol()
		finalize_at = DateTimeCol(default=None)
		who_win = StringCol(length=1, default=None)


class BettingHistory(SQLObject):
		user_who_bet = ForeignKey('User')
		evento = ForeignKey('Evento')
		option_selected = StringCol()
		bet_on = DateTimeCol(default=DateTimeCol.now)
		amount_bet = FloatCol(default=0.0)
		
class BettingPayments(SQLObject):
		user = ForeignKey('User')
		evento = ForeignKey('Evento')
		value_won = FloatCol(default=0.0)
		hour_of_payment = DateTimeCol(default=DateTimeCol.now)