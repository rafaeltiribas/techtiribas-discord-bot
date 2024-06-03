from src.models.bot_bank import BotBank

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from src.models.wallet import Wallet
from src.models.user import Role
from user_service import UserService

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
			                    cron_execute_diary_tax="1 * * * *",
			                    cron_execute_daily_prize="0 6,18 * * *")
	
	
	def start_taxes_scheduller(self):
		self.sched.add_job(self.execute_diary_tax_in_wallets, self.trigger)
		self.sched.start()
	
	def execute_diary_tax_in_wallets(self):
		print(f'Rendendo {self.bank.diary_tax} em todas as Wallets')
		for w in Wallet.select():
			w.balance = round(w.balance + ((self.bank.diary_tax / 100) * w.balance), 2)
			
	def execute_diary_prizes(self):
		print(f'Iniciar a premiação diária')
		
		
	def alter_diary_tax(self, ctx, new_tax, new_cron):
		user = UserService.get_user_by_ctx(ctx)
		if user is None or user.role is not Role.Council.name:
			raise ValueError(f'Usuário não encontrado ou não autorizado!')
		
		self.bank.balance = new_tax
		self.bank.cron_execute_diary_tax = new_cron