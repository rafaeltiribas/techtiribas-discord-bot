from src.models.bot_bank import BotBank

from src.services.jobs_service import JobsService
from src.models.wallet import Wallet
from src.models.user import Role
from src.services.user_service import UserService

import src.functionalities.log as LOG



class BotBankService:
		user_service = UserService()
		jobs_service = JobsService()
		def __init__(self):
				self.init_bank()
				self.start_taxes_scheduler()
				
		def init_bank(self):
				self.bank = BotBank.select().getOne(None)
				if self.bank is None:
						self.bank = BotBank(diary_tax=1.5, daily_prize=20.0,
						                    cron_execute_diary_tax="1 * * * *",
						                    cron_execute_daily_prize="0 6,18 * * *")
		
		def start_taxes_scheduler(self):
				self.jobs_service.new_job("diary_taxes", self.bank.cron_execute_diary_tax, self.execute_diary_tax_in_wallets)
				self.jobs_service.new_job("diary_prizes", self.bank.cron_execute_daily_prize, self.execute_daily_prize)
		
		def execute_diary_tax_in_wallets(self):
				LOG.info(f'Rendendo {self.bank.diary_tax} em todas as Wallets')
				for w in Wallet.select():
						w.balance = round(w.balance + ((self.bank.diary_tax / 100) * w.balance), 2)
		
		def execute_daily_prize(self):
				LOG.info(f'Iniciar a premiação diária')
		
		def alter_diary_tax(self, ctx, new_tax, new_cron):
				user = self.user_service.get_user_by_ctx(ctx)
				if user is None or user.role is not Role.Council.name:
						raise ValueError(f'Usuário não encontrado ou não autorizado!')
				
				self.bank.balance = new_tax
				self.bank.cron_execute_diary_tax = new_cron
