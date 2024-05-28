"""Reune todos os comandos disponíveis no bot.

Os comandos precisam obrigatoriamente de um parâmetro de contexto.
Este parâmetro está sendo chamado convencionalmente de `ctx`.
"""

from random import randint

import requests
from discord.ext import commands

ROADMAP_URL = 'https://raw.githubusercontent.com/rafaeltiribas/techtiribas/main/roadmap/README.md'


@commands.command('salve', help='Responde uma saudação.')
async def hello(ctx):
    """Responde uma saudação."""
    await ctx.send('Salvi')


@commands.command('dice', help='Rola um dado.')
async def roll_dice(ctx):
    """Rola um dado."""
    await ctx.send(randint(1, 6))


@commands.command('roadmap', help='Mostra o roadmap das lives.')
async def roadmap(ctx):
    """Mostra o roadmap das lives."""
    await ctx.send(requests.get(ROADMAP_URL))
