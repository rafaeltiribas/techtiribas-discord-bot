from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.base import SchedulerAlreadyRunningError
from apscheduler.schedulers.base import JobLookupError
import src.utils.log as LOG

"""
	Este service serve para manter jobs, pode-se obter um, criar e deletar (famoso CRUD)
	
	No Bot existe jobs que deverão ser executados quando um tal dia ou hora
		chegar
"""

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
				self.scheduler.add_job(def_to_execute, trigger, id=job_id)
				self.scheduler.start()
				LOG.info(f'Novo job registrado: {job_id}')
			except SchedulerAlreadyRunningError:
				LOG.warn(f"Já existe um job '{job_id}' em execução.")

	def get_especific_job(self, job_id):
		job = self.scheduler.get_job(job_id)
		msg = f"Não foi encontrado o job '{job_id}'"
		if job is not None:
			msg = f"ID: {job.id}, Função a ser executada: {job.func.__name__}, Próxima Execução: {job.next_run_time}"
		return msg
	
	
	def get_job(self, job_id):
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

	def kill_job(self, job_id):
		try:
			self.scheduler.remove_job(job_id)
			LOG.info(f"Job '{job_id}' removido com sucesso.")
		except JobLookupError:
			LOG.info(f"O job com ID '{job_id}' não foi encontrado.")
			
	def kill_all_jobs(self):
		count = len(self.scheduler.get_jobs())
		self.scheduler.remove_all_jobs()
		msg = f"{count} Jobs removidos com sucesso."
		LOG.info(msg)
		return msg
