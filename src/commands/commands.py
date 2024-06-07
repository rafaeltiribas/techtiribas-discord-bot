"""Reune todos os comandos disponíveis no bot.

Os comandos precisam obrigatoriamente de um parâmetro de contexto.
Este parâmetro está sendo chamado convencionalmente de `ctx`.
"""

from random import randint

import requests
from discord.ext import commands as com
import time

from src.exceptions.bot_errors import UserError
from src.services.user_service import UserService
from src.services.wallet_service import WalletService
import src.functionalities.messages as message

ROADMAP_URL = 'https://raw.githubusercontent.com/rafaeltiribas/techtiribas/main/roadmap/README.md'

usr_service = UserService()
wallet_service = WalletService()


@com.hybrid_command(help='Responde uma saudação.')
async def salve(ctx):
		"""Responde uma saudação."""
		await message.send_msg_in_ctx(ctx, 'Salvi')


@com.hybrid_command(help='Rola um dado.')
async def dice(ctx):
		"""Rola um dado."""
		await message.send_msg_in_ctx(ctx, randint(1, 6))


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
		try:
				msg_resp = usr_service.register_user_from_ctx(ctx)
				await ctx.send(msg_resp, ephemeral=True)
		except UserError as ue:
				await ctx.send(ue.mensagem, ephemeral=True)


def setup(bot):
		"""defina aqui os comandos no bot"""
		bot.add_command(ping)
		bot.add_command(roadmap)
		bot.add_command(dice)
		bot.add_command(salve)
		bot.add_command(register)
