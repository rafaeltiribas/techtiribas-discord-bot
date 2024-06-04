from src.models.user_interactions import UserInteractionsHistory, UserInteractions
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import src.utils.log as LOG

class UserInteractionsService:
	
	def all_interactions(self):
		return UserInteractionsHistory.select()
	
	def all_users_who_interacted(self):
		all_interactions = self.all_interactions()
		users = [interaction.user for interaction in all_interactions]
		return users
	
	
	
	"""Inicia schedules"""
	def start_schedules(self):
		self.sched = BackgroundScheduler()
		user_interaction_config = UserInteractions.select()
		self.trigger = CronTrigger.from_crontab(user_interaction_config.cron_execute_periodic_cleaning)
		self.execute_cron_tasks()
		
	def execute_cron_tasks(self):
		self.sched.add_job(self.realize_periodic_cleaning, self.trigger)
		self.sched.start()
	
	def realize_periodic_cleaning(self):
		UserInteractionsHistory.deleteAll()
		LOG.info_highlighted("Limpeza de interacoes dos usuários foram feitas com sucesso")