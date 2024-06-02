from sqlobject import SQLObject, StringCol, FloatCol

"""
	Crontab é um cron expression
	cada cron_execute_ é um cron que será executado de acordo com ela
	para gerar um, ou entender, acesse -> https://crontab.guru/
	
	o diary_tax é a taxa que as wallets vão render por dia, como um CDB
	o prize é o valor a ser distribuído por dia, se o user interagir de alguma forma
	
"""

class BotBank(SQLObject):
	diary_tax = FloatCol()
	daily_prize = FloatCol()
	cron_execute_diary_tax = StringCol()
	cron_execute_daily_prize = StringCol()