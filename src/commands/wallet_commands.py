from discord.ext import commands as com
from discord import app_commands
import discord
import random

from src.services.user_service import UserService
from src.services.wallet_service import WalletService
import src.utils.messages as message

user_service = UserService()
wallet_service = WalletService()

@com.hybrid_command('bytes', help="Consulte seu saldo de Bytes e ganhe um premio")
async def consulting_bytes(ctx: com.Context):
	try:
		msg = wallet_service.get_balance_wallet(ctx)
		embed = message.gen_embed_message("Seus bytes", msg, discord.Color.gold())
		await message.send_embed_with_img(ctx, embed, 'mask_money.gif', True)
	except ValueError as e:
		msg = message.gen_embed_message("Deu ruim...", e, discord.Color.red())
		await message.send_embed_with_img(ctx, msg, 'dois_burro.jpg', True)

@com.hybrid_command(help="Transfira uma parte dos seus bytes mas SEM JUROS!")
@app_commands.describe(username="Marque o usuário", bytes="Valor em Bytes. ex: 300,00")
async def transferir_bytes(ctx: com.Context, username: str, bytes: float):
	try:
		msg = wallet_service.transferir_bytes_para(ctx, username, bytes)
		embed = message.gen_embed_message("Transferência", msg, discord.Color.green(), footer=transferencia_entre_pobres())
		await message.send_embed_with_img(ctx, embed, 'transferencia_monkey.gif', True)
	except ValueError as e:
		msg = message.gen_embed_message("Deu ruim...", e, discord.Color.red())
		await message.send_embed_with_img(ctx, msg, 'dois_burro.jpg', True)

def setup(bot):
	"""defina aqui os comandos no bot"""
	bot.add_command(consulting_bytes)
	bot.add_command(transferir_bytes)


def transferencia_entre_pobres():
    frases = [
        "Gaste tudo de uma vez no cassino :smiling_imp:",
        "Compre meio chiclete seu mendigo",
        "Aproveite sua nova riqueza de dois centavos",
        "Não deixe essa riqueza de porco subir à cabeça",
        "Invista esse montante, gire a roleta no cassino :smiling_imp:",
        "A riqueza está próxima, só nascer denovo",
        "Compre algo na promoção de 10 centavos",
        "Você está a um centavo de ser pobre, mendigo já é",
	      "Dá até para sonhar com um Méqui! Mas só sonhar."
    ]
    return random.choice(frases)