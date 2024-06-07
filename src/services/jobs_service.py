import discord
from src.models.user import *
from src.services.user_service import *
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.base import SchedulerAlreadyRunningError
from apscheduler.schedulers.base import JobLookupError
import src.functionalities.log as LOG

"""
	Este service serve para manter jobs, pode-se obter um, criar e deletar (famoso CRUD)
	
	No Bot existe jobs que deverão ser executados quando um tal dia ou hora
		chegar
"""

user_service = UserService()

class JobsService:
		
		def __init__(self):
				self.scheduler = BackgroundScheduler()
		
		"""
			Este def serve justamente para "agendar" novos jobs
			
			* job_id -> marcar job com um id, para ele ser único
			* cron_expression -> consulte o https://crontab.guru/ ou procure no google
			* def_to_execute -> o def que será executado de acordo
					com o dia e hora definido no cron_expression
		"""
		
		def new_job(self, job_id, cron_expression, def_to_execute):
				trigger = CronTrigger.from_crontab(cron_expression)
				if self.scheduler.get_job(job_id) is None:
						try:
								job = self.scheduler.add_job(func=def_to_execute, trigger=trigger, id=job_id)
								LOG.info(f'Novo job registrado para execução: {job.id}')
						except SchedulerAlreadyRunningError as se:
								LOG.warn(f"Já existe um job '{job_id}' em execução.")
		
		def start_jobs(self, interaction : discord.Interaction):
				self.validate_if_user_can_manage_jobs(interaction)
				try:
						self.scheduler.start()
						LOG.info("Jobs iniciados...")
						return "Iniciado todos os jobs"
				except SchedulerAlreadyRunningError as se:
						LOG.warn(f"Houve um erro ao tentar iniciar jobs: {se}")
						raise AdminError(f"Jobs já foram iniciados!")
				except Exception as e:
						LOG.error(f"Erro interno ao iniciar jobs: {e}")
						raise e
		
		def get_especific_job(self, interaction : discord.Interaction, job_id):
				self.validate_if_user_can_manage_jobs(interaction)
				job = self.scheduler.get_job(job_id)
				msg = f"Não foi encontrado o job '{job_id}'"
				if job is not None:
						LOG.text_highlighted(f"Job id {job.id}")
						msg = f"ID: {job.id}, Função a ser executada: {job.func.__name__}, Próxima Execução: {job.next_run_time}"
				LOG.text_highlighted(msg)
				return msg
		
		def get_job(self, interaction : discord.Interaction, job_id):
				self.validate_if_user_can_manage_jobs(interaction)
				return self.scheduler.get_job(job_id)
		
		def list_jobs(self):
				jobs = self.scheduler.get_jobs()
				if len(jobs) > 0:
						LOG.info_highlighted("Lista de Jobs rodando atualmente:")
						for job in jobs:
								LOG.info(f"ID: {job.id}, Função a ser executada: {job.func.__name__}, Próxima Execução: {job.next_run_time}")
				else:
						LOG.info("Não há jobs em execução")
				return jobs
		
		def kill_job(self, interaction : discord.Interaction, job_id):
				self.validate_if_user_can_manage_jobs(interaction)
				try:
						self.scheduler.remove_job(job_id)
						LOG.info(f"Job '{job_id}' removido com sucesso.")
				except JobLookupError:
						LOG.info(f"O job com ID '{job_id}' não foi encontrado.")
		
		def kill_all_jobs(self, interaction: discord.Interaction):
				self.validate_if_user_can_manage_jobs(interaction)
				count = len(self.scheduler.get_jobs())
				self.scheduler.remove_all_jobs()
				msg = f"{count} Jobs removidos com sucesso."
				LOG.info(msg)
				return msg
		
		def validate_if_user_can_manage_jobs(self, interaction : discord.Interaction):
				if not user_service.user_is_admin_or_higher(interaction):
						raise UserError("Você não tem autorização para fazer isso!")
