import os

from discord import Intents
from discord.ext import commands as com
from dotenv import find_dotenv, load_dotenv

import commands

# GET TOKEN
load_dotenv(find_dotenv('.venv/.env'))
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurando as necessidades do bot: Ler e enviar mensagens
intents = Intents.all()
intents.message_content = True


class TiribasBot(com.Bot):
    """Estende a classe base Bot."""

    async def on_ready(self):
        """Evento de inicialização."""
        print(f'{self.user} está rodando')
        await self.tree.sync()

    async def on_command_error(self, ctx, error) -> None:
        """Lida com erros no comando."""
        print(error)
        if isinstance(error, com.errors.CommandError):
            await ctx.send('Alguma coisa deu errado ao executar esse comando. Fale com os adms')


bot = TiribasBot(command_prefix='/', intents=intents)

commands.setup(bot)

if __name__ == '__main__':
    bot.run(TOKEN)
