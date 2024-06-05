"""Reune todos os comandos disponíveis no bot.

Os comandos precisam obrigatoriamente de um parâmetro de contexto.
Este parâmetro está sendo chamado convencionalmente de `ctx`.
"""

from random import randint

import requests
from discord.ext import commands as com
from discord import app_commands
import time

from src.services.user_service import UserService
from src.services.wallet_service import WalletService
import src.utils.messages as message


ROADMAP_URL = 'https://raw.githubusercontent.com/rafaeltiribas/techtiribas/main/roadmap/README.md'

usr_service = UserService()
wallet_service = WalletService()

@com.hybrid_command(help='Responde uma saudação.')
async def salve(ctx):
	"""Responde uma saudação."""
	await message.send_msg(ctx, 'Salvi')


@com.hybrid_command(help='Rola um dado.')
async def dice(ctx):
	"""Rola um dado."""
	await message.send_msg(ctx, randint(1, 6))


@com.hybrid_command(help='Mostra o roadmap das lives.')
async def roadmap(ctx):
	"""Mostra o roadmap das lives."""
	await ctx.send(requests.get(ROADMAP_URL), mention_author=True)


@com.hybrid_command(help="Dá um ping, toma um pong")
async def ping(ctx: com.Context):
	"""Clássica resposta depois de um ping"""
	start_time = time.time()
	msg = await ctx.send("Calculando ping...")
	end_time = time.time()
	ms = (end_time - start_time) * 1000
	
	await msg.edit(content=f"pong! Latência está em {ms:.2f} ms")

@com.hybrid_command(help="Faça seu cadastro no Bot")
async def register(ctx: com.Context):
	msg = await ctx.send("Registrando...", mention_author=True)
	msg_resp = usr_service.register_user_from_ctx(ctx)
	await msg.edit(content=msg_resp)


@com.hybrid_command('alterar_funcao', help="Altere um usuário para Member, Subscriber ou Admin")
@app_commands.describe(username="Marque o usuário", role="Member, Subscriber ou Admin")
async def update_role_user(ctx: com.Context, username: str, role: str):
	msg_resp = usr_service.update_user_role(ctx, username, role)
	await message.send_msg(ctx, msg_resp, True)


def setup(bot):
	"""defina aqui os comandos no bot"""
	bot.add_command(ping)
	bot.add_command(roadmap)
	bot.add_command(dice)
	bot.add_command(salve)
	bot.add_command(register)
	bot.add_command(update_role_user)