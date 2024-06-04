import os
import src.utils.log as LOG

from discord import Intents
import discord
from discord.ext import commands as com
from dotenv import find_dotenv, load_dotenv
from db import database_config
from src.services.bot_bank_service import BotBankService
from src.services.user_interactions_service import UserInteractionsService
import src.utils.messages as message
from src.commands import commands, admin_commands, wallet_commands

# GET TOKEN
load_dotenv(find_dotenv('.venv/.env'))
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurando as necessidades do bot: Ler e enviar mensagens
intents = Intents.all()
intents.message_content = True

database_config.init_db()
database_config.create_tables()

bank = BotBankService()
interactions = UserInteractionsService()
interactions.init_bank()
interactions.start_schedules()

class TiribasBot(com.Bot):
	"""Estende a classe base Bot."""
	
	async def on_ready(self):
		"""Evento de inicialização."""
		LOG.info_highlighted(f'{self.user} está rodando')
		await self.tree.sync()
	
	async def on_command_error(self, ctx, error) -> None:
		"""Lida com erros no comando."""
		LOG.error(error)
		if isinstance(error, com.errors.CommandNotFound):
			msg = message.gen_embed_message("Deu ruim...", error, discord.Color.red())
			await message.send_embed_with_img(ctx, msg, 'not-stonks-meme.gif', True)
		elif isinstance(error, com.errors.CommandError):
			msg = message.gen_embed_message("Deu ruim...", error, discord.Color.red())
			await message.send_embed_with_img(ctx, msg, 'not-stonks-meme.gif', True)


bot = TiribasBot(command_prefix='/', intents=intents)

commands.setup(bot)
admin_commands.setup(bot)
wallet_commands.setup(bot)

if __name__ == '__main__':
	bot.run(TOKEN)
