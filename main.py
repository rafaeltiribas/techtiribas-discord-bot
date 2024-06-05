import os

from discord.ext.commands import Context, errors
from discord.ext.commands._types import BotT

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
		
		async def on_slash_command_error(self, ctx, error) -> None:
				"""Lida com erros no comando."""
				LOG.error_highlighted(error)
				if isinstance(error, com.errors.CommandNotFound):
						msg = message.gen_embed_message("Que comando é esse?", error, discord.Color.red())
						await message.send_embed_with_img_to_ctx(ctx, msg, 'dois_burro.jpg', True)
				elif isinstance(error, com.errors.CommandError):
						msg = message.gen_embed_message("Deu ruim...", error, discord.Color.red())
						await message.send_embed_with_img_to_ctx(ctx, msg, 'not-stonks-meme.gif', True)


bot = TiribasBot(command_prefix='/', intents=intents)

commands.setup(bot)
wallet_commands.WalletCommands(bot)
admin_commands.AdminCommands(bot)

if __name__ == '__main__':
		bot.run(TOKEN)
