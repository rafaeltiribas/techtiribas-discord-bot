from discord.ext import commands as com
from discord import app_commands
import discord
import random

from src.services.user_service import UserService
from src.services.wallet_service import WalletService
from src.exceptions.bot_errors import UserError
import src.utils.messages as message

user_service = UserService()
wallet_service = WalletService()


class WalletCommands(com.Cog):
		def __init__(self, bot):
				self.bot = bot
				self.bot.tree.add_command(self.wallet_command)
		
		wallet_command = app_commands.Group(name="bytes",
		                                    description="Manipule seus bytes")
		
		@wallet_command.command(name='saldo', description="Consulte seu saldo de Bytes e ganhe um premio")
		async def consulting_bytes(self, interaction: discord.Interaction):
				try:
						msg = wallet_service.get_balance_wallet(interaction)
						embed = message.gen_embed_message("Seus bytes", msg, discord.Color.gold())
						await message.send_embed_with_img(interaction, embed, 'mask_money.gif', True)
				except UserError as e:
						await message.send_user_error_msg(interaction, e)
		
		@wallet_command.command(name='transferir', description="Transfira uma parte dos seus bytes mas SEM JUROS!")
		@app_commands.describe(username="Marque o usuário", bytes="Valor em Bytes. ex: 300,00")
		async def transferir_bytes(self, interaction: discord.Interaction, username: str, bytes: float):
				try:
						msg = wallet_service.transferir_bytes_para(interaction, username, bytes)
						embed = message.gen_embed_message("Transferência", msg, discord.Color.green(),
						                                  footer=self.transferencia_entre_pobres())
						await message.send_embed_with_img(interaction, embed, 'transferencia_monkey.gif', True)
				except UserError as e:
						await message.send_user_error_msg(interaction, e)
		

		def transferencia_entre_pobres(self):
				frases = [
						"Gaste tudo de uma vez no cassino",
						"Compre meio chiclete seu mendigo",
						"Aproveite sua nova riqueza de dois centavos",
						"Não deixe essa riqueza de porco subir à cabeça",
						"Invista esse montante, gire a roleta no cassino",
						"A riqueza está próxima, só nascer denovo",
						"Compre algo na promoção de 10 centavos",
						"Você está a um centavo de ser pobre, mendigo já é",
						"Dá até para sonhar com um Méqui! Mas só sonhar."
				]
				return random.choice(frases)
