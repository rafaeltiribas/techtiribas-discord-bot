import discord
from discord import app_commands
from discord.ext import commands as com

import src.functionalities.messages as message
from src.models.user import Role
from src.exceptions.bot_errors import *
from src.services.jobs_service import JobsService
from src.services.user_service import UserService

jobs_service = JobsService()
user_service = UserService()


class AdminCommands(com.Cog):
		
		def __init__(self, bot):
				self.bot = bot
				self.bot.tree.add_command(self.admin)
		
		admin = app_commands.Group(name="staff", description="Comandos de Adm ou maior, não se atreva ou haverá punições ")
		
		@admin.command(name='finalizar_todos_jobs', description="Mate os jobs")
		async def kill_jobs(self, interaction: discord.Interaction):
				try:
						msg = jobs_service.kill_all_jobs(interaction)
						embed = message.gen_embed_message(
								title="Matando serviço né...",
								description=msg,
								color=discord.Color.pink(),
						)
						await message.send_embed_with_img(interaction, embed, "staff", "finalizar_todos_jobs")
				except UserError as ue:
						await message.send_user_error_msg(interaction, ue)
				except Exception as e:
						await message.send_std_error_msg(interaction, e)
		
		@admin.command(name='job', description="Veja o que rola num job process")
		@app_commands.describe(job_id="Id do job")
		async def get_especific_job(self, interaction: discord.Interaction, job_id: str):
				try:
						msg = jobs_service.get_especific_job(interaction, job_id)
						embed = message.gen_embed_message(
								title="Job",
								description=msg,
								color=discord.Color.blurple()
						)
						await message.send_embed_with_img(interaction, embed, "staff", "admin")
				except UserError as ue:
						await message.send_user_error_msg(interaction, ue)
		
		@admin.command(name='jobs', description="Lista todos os bots")
		async def list_all_jobs(self, interaction: discord.Interaction):
				try:
						fields = jobs_service.list_jobs(interaction)
						embed = message.gen_embed_message(
								title="Jobs em execução",
								description="Se liga nos jobs...",
								fields=fields,
								color=discord.Color.blurple()
						)
						await message.send_embed_with_img(interaction, embed, "staff", "admin")
				except UserError as ue:
						await message.send_user_error_msg(interaction, ue)
				except Exception as e:
						await message.send_std_error_msg(interaction, e)
		
		@admin.command(name='alterar_funcao', description="Altere um usuário para Member, Subscriber ou Admin")
		@app_commands.describe(username="Marque o usuário", role="Member, Subscriber ou Admin")
		@app_commands.choices(role = [
				app_commands.Choice(name=role.name, value=role.name)
				for role in Role
		])
		async def update_role_user(self, interaction: discord.Interaction, username: str, role: str):
				try:
						msg_resp = user_service.update_user_role(interaction, username, role)
						await message.send_embed_msg(interaction, msg_resp)
				except UserError as ue:
						await message.send_user_error_msg(interaction, ue)
				except AdminError as ae:
						await message.send_std_error_msg(interaction, ae)
