from sqlobject import SQLObject, StringCol, ForeignKey, DateTimeCol


class UserInteractions(SQLObject):
		cron_execute_periodic_cleaning = StringCol()


class UserInteractionsHistory(SQLObject):
		user = ForeignKey('User')
		time_iteracted = DateTimeCol()
