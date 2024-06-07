import discord
from discord import app_commands
from discord.ext import commands as com

import src.functionalities.messages as message
from src.models.evento import Category
from src.services.jobs_service import JobsService
from src.services.user_service import UserService
from src.services.evento_service import EventoService
from src.exceptions.bot_errors import UserError

jobs_service = JobsService()
user_service = UserService()
evento_service = EventoService()


class EventoCommands(com.Cog):
		
		def __init__(self, bot):
				self.bot = bot
				self.bot.tree.add_command(self.evento)
		
		evento = app_commands.Group(name="evento", description="Gerencie eventos no server!")
		
		@evento.command(name='criar', description="Crie um evento")
		@app_commands.describe(titulo="Titulo do Evento", categoria="De qual categoria?", opcao_a="Nome da opção",
		                       opcao_b="Nome da opção")
		async def create(self, interaction: discord.Interaction, titulo: str, categoria: str, opcao_a: str, opcao_b: str):
				evt = evento_service.create_event(interaction, titulo, categoria, opcao_a, opcao_b)
				await message.announce_event(interaction, evt)
		
		@evento.command(name='apostar', description="Aposte em um evento")
		@app_commands.describe(id="Id do evento", opcao="Qual sua opção?", bytes="Quantidade de bytes")
		async def bet_on_the_event(self, interaction: discord.Interaction, id: int, opcao: str, bytes: float):
				try:
						field_response = evento_service.betting_on(interaction, id, opcao, bytes)
						embed = message.gen_embed_message(
								title="Apostado!",
								description="Dados da aposta:",
								color=discord.Color.green(),
								fields=field_response
						)
						await message.send_embed_with_img(interaction, embed, 'bet_feita.gif')
				except UserError as ue:
						await message.send_user_error_msg(interaction, ue, True)
				except Exception as e:
						await message.send_std_error_msg(interaction, e)
		
		@evento.command(name='anunciar', description="Anuncie um evento")
		@app_commands.describe(id="Id do evento")
		async def announce_event(self, interaction: discord.Interaction, id: int):
				try:
						evt = evento_service.get_event_to_announce(interaction, id)
						await message.announce_event(interaction, evt)
				except UserError as ue:
						await message.send_user_error_msg(interaction, ue, True)
				except Exception as e:
						await message.send_std_error_msg(interaction, e)
		
		@evento.command(name='fechar', description="Fechar as apostas")
		@app_commands.describe(id="Id do evento")
		async def close_bets(self, interaction: discord.Interaction, id: int):
				try:
						closed_embed_msg = evento_service.close_bets(interaction, id)
						await message.send_embed_with_img(interaction, closed_embed_msg, 'closed_bets.gif', False)
				except UserError as ue:
						await message.send_user_error_msg(interaction, ue, True)
				except Exception as e:
						await message.send_std_error_msg(interaction, e)
		
		@evento.command(name='finalizar', description="Finalizar evento, declarar vencedor e realizar os pagamentos")
		@app_commands.describe(id="Id do evento", vencedor="Quem ganhou?")
		async def finalize_evento(self, interaction: discord.Interaction, id: int, vencedor: str):
				try:
						embed_msg = evento_service.finalize_events(interaction, id, vencedor)
						await message.send_embed_with_img(interaction, embed_msg, 'congrats_winners.gif', False)
				except UserError as ue:
						await message.send_user_error_msg(interaction, ue, True)
				except Exception as e:
						await message.send_std_error_msg(interaction, e)
		
		@bet_on_the_event.autocomplete('opcao')
		async def _opcoes(self, interaction: discord.Interaction, current: str):
				options = [
						app_commands.Choice(name="A", value="A"),
						app_commands.Choice(name="B", value="B"),
				]
				return [choice for choice in options if current.lower() in choice.name.lower()]
		
		@create.autocomplete('categoria')
		async def _list_categories(self, interaction: discord.Interaction, current: str):
				return [
						app_commands.Choice(name=category.value, value=category.name)
						for category in Category
						if current.lower() in category.value.lower()
				]
		
		@finalize_evento.autocomplete('vencedor')
		async def _opcoes_winner(self, interaction: discord.Interaction, current: str):
				options = [
						app_commands.Choice(name="A", value="A"),
						app_commands.Choice(name="B", value="B"),
				]
				return [choice for choice in options if current.lower() in choice.name.lower()]
