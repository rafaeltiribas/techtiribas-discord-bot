import os

from discord import Intents
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv

from commands import hello, roadmap, roll_dice

# GET TOKEN
load_dotenv(find_dotenv('.venv/.env'))
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurando as necessidades do bot: Ler e enviar mensagens
intents = Intents.default()
intents.message_content = True


class MyBot(commands.Bot):
    """Estende a classe base Bot."""

    async def on_ready(self):
        """Evento de inicialização."""
        print(f'{self.user} está rodando')

    async def on_command_error(self, ctx, error) -> None:
        """Lida com erros no comando."""
        print(error)
        if isinstance(error, commands.errors.CommandError):
            await ctx.send('Alguma coisa deu errado ao executar esse comando.')


bot = MyBot(command_prefix='=', intents=intents)
bot.add_command(hello)
bot.add_command(roll_dice)
bot.add_command(roadmap)


if __name__ == '__main__':
    bot.run(TOKEN)
