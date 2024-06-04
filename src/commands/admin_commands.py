from discord.ext import commands as com
from discord import app_commands
import discord
from src.services.jobs_service import JobsService
from src.services.user_service import UserService

import src.utils.messages as message

jobs_service = JobsService()
user_service = UserService()


@com.hybrid_command(help='Limpeza de jobs')
async def kill_jobs(ctx):
	if not (user_service.user_is_admin_or_higher(ctx)):
		await ctx.send("Você não está autorizado a realizar essa ação", ephemeral=True)
		return
	
	msg = jobs_service.kill_all_jobs()
	fields = {
		"Resposta": {"value": msg, "inline": True}
	}
	embed = message.gen_embed_message(
		title="/kill_jobs",
		description="Admin command",
		color=discord.Color.yellow(),
		fields=fields,
		# author={"name": "Admin command"},
		footer=f"Executed by {ctx.author.name}",
		# url_img=""
	)
	await message.send_embed_with_img(ctx, embed, 'admin.gif', True)


@com.hybrid_command('get_job', help='Sobre um job')
@app_commands.describe(job_id="Id do job")
async def get_especific_job(ctx, job_id: str):
	if not (user_service.user_is_admin_or_higher(ctx)):
		await ctx.send("Você não está autorizado a realizar essa ação", ephemeral=True)
		return
	
	msg = jobs_service.get_especific_job(job_id)
	await ctx.author.send(msg)


def setup(bot):
	"""defina aqui os comandos no bot"""
	bot.add_command(kill_jobs)
	bot.add_command(get_especific_job)
