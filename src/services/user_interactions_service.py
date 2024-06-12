from src.models.user_interactions import UserInteractionsHistory, UserInteractions
from src.models.user import User
import src.functionalities.cron_expressions as cron_exp
from datetime import datetime
from src.services.jobs_service import JobsService
import src.functionalities.log as LOG


class UserInteractionsService:
		jobs_service = JobsService()
		
		def init_bank(self):
				self.user_interaction_config = UserInteractions.select().getOne(None)
				if self.user_interaction_config is None:
						cron = "0 3 * * *"
						LOG.info(f'Configuracao de limpeza de interacoes do usuário criada e marcada para {cron_exp.get_datetime(cron)}')
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
				interactions = list(UserInteractionsHistory.selectBy(user=user))
				if interactions is None:
						return False
				return len(interactions) > 0
		
		def get_config_interactions(self):
				return UserInteractions.select().getOne(None)
		
		"""Inicia schedules"""
		
		def start_schedules(self):
				self.jobs_service.new_job("periodic_cleaning", self.get_config_interactions().cron_execute_periodic_cleaning,
				                          self.realize_periodic_cleaning)
		
		def realize_periodic_cleaning(self):
				UserInteractionsHistory.deleteMany(None)
				LOG.info_highlighted("Limpeza de interacoes dos usuários foram feitas com sucesso")
