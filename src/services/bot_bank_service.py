from src.models.bot_bank import BotBank

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.models.wallet import Wallet

class BotBankService:
	
	def __init__(self):
		self.init_bank()
		self.sched = BackgroundScheduler()
		self.trigger = CronTrigger.from_crontab(self.bank.cron_execute_diary_tax)
		self.start_taxes_scheduller()
	
	def init_bank(self):
		self.bank = BotBank.select().getOne(None)
		if self.bank is None:
			self.bank = BotBank(diary_tax=1.5, daily_prize=20.0,
			                    cron_execute_diary_tax="* * * * *",
			                    cron_execute_daily_prize="* * * * *")
	
	
	def start_taxes_scheduller(self):
		self.sched.add_job(self.execute_diary_tax_in_wallets, self.trigger)
		self.sched.start()
	
	def execute_diary_tax_in_wallets(self):
		print(f'Rendendo {self.bank.diary_tax} em todas as Wallets')
		for w in Wallet.select():
			w.balance = round(w.balance + ((self.bank.diary_tax / 100) * w.balance), 2)