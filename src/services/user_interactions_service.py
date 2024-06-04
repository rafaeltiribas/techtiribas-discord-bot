from src.models.user_interactions import UserInteractionsHistory, UserInteractions
from src.models.user import User
import src.utils.cron_expressions as cron_exp
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import src.utils.log as LOG

class UserInteractionsService:
		
	def init_bank(self):
		self.user_interaction_config = UserInteractions.select().getOne(None)
		if self.user_interaction_config is None:
			cron = "0 3 * * *"
			LOG.info(f'Configuracao de limpeza de interacoes do usuário marcada para {cron_exp.get_datetime(cron)}')
			self.user_interaction_config = UserInteractions(
				cron_execute_periodic_cleaning=cron
			)
	
	def all_interactions(self):
		return UserInteractionsHistory.select()
	
	def all_users_who_interacted(self):
		all_interactions = self.all_interactions()
		users = [interaction.user for interaction in all_interactions]
		return users
	
	def add_user(self, user: User):
		UserInteractionsHistory(user=user, time_iteracted=datetime.now())
	
	def has_already_interacted(self, user: User):
		interactions = UserInteractionsHistory.selectBy(user=user)
		if interactions is None:
			return False
		else:
			return True
	
	"""Inicia schedules"""
	def start_schedules(self):
		self.sched = BackgroundScheduler()
		self.trigger = CronTrigger.from_crontab(self.user_interaction_config.cron_execute_periodic_cleaning)
		self.execute_cron_tasks()
		
	def execute_cron_tasks(self):
		id = "periodic_cleaning"
		if not self.sched.get_job(id):
			self.sched.add_job(self.realize_periodic_cleaning, self.trigger, id=id)
			self.sched.start()
	
	def realize_periodic_cleaning(self):
		UserInteractionsHistory.deleteAll()
		LOG.info_highlighted("Limpeza de interacoes dos usuários foram feitas com sucesso")