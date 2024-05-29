"""Reune todos os comandos disponíveis no bot.

Os comandos precisam obrigatoriamente de um parâmetro de contexto.
Este parâmetro está sendo chamado convencionalmente de `ctx`.
"""

from random import randint

import requests
from discord.ext import commands as com
import time

ROADMAP_URL = 'https://raw.githubusercontent.com/rafaeltiribas/techtiribas/main/roadmap/README.md'


@com.hybrid_command(help='Responde uma saudação.')
async def salve(ctx):
    """Responde uma saudação."""
    await ctx.send('Salvi')


@com.hybrid_command(help='Rola um dado.')
async def dice(ctx):
    """Rola um dado."""
    await ctx.send(randint(1, 6))


@com.hybrid_command(help='Mostra o roadmap das lives.')
async def roadmap(ctx):
    """Mostra o roadmap das lives."""
    await ctx.send(requests.get(ROADMAP_URL))
