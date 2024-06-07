import discord
from discord import app_commands
from discord.ext import commands as com

import src.functionalities.messages as message
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
				if not user_service.user_is_admin_or_higher(interaction):
						await interaction.response.send_message("Você não está autorizado a realizar essa ação", ephemeral=True)
						return
				
				msg = jobs_service.kill_all_jobs()
				fields = {
						"Resposta": {"value": msg, "inline": False}
				}
				embed = message.gen_embed_message(
						title="/kill_jobs",
						description="Admin command",
						color=discord.Color.yellow(),
						fields=fields,
						footer=f"Executed by {interaction.user.name}"
				)
				await message.send_embed_with_img(interaction, embed, 'admin.gif', True)
		
		@admin.command(name='job', description="Veja o que rola num job process")
		@app_commands.describe(job_id="Id do job")
		async def get_especific_job(self, interaction: discord.Interaction, job_id: str):
				if not user_service.user_is_admin_or_higher(interaction):
						await interaction.response.send_message("Você não está autorizado a realizar essa ação", ephemeral=True)
						return
				
				msg = jobs_service.get_especific_job(job_id)
				embed = message.gen_embed_message(
						title="Job",
						description=msg,
						color=discord.Color.blurple()
				)
				await message.send_embed_with_img(interaction, embed, 'admin.gif')
		
		@admin.command(name='iniciar_jobs', description="Inicia todos os jobs do bot")
		async def start_jobs(self, interaction: discord.Interaction):
				msg = jobs_service.start_jobs()
				embed = message.gen_embed_message(
						title="Job",
						description=msg,
						color=discord.Color.blurple()
				)
				await message.send_embed_with_img(interaction, embed, 'admin.gif')
		
		@admin.command(name='alterar_funcao', description="Altere um usuário para Member, Subscriber ou Admin")
		@app_commands.describe(username="Marque o usuário", role="Member, Subscriber ou Admin")
		async def update_role_user(self, interaction: discord.Interaction, username: str, role: str):
				msg_resp = user_service.update_user_role(interaction, username, role)
				await message.send_msg_in_ctx(interaction, msg_resp)
