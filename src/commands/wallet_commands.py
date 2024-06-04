from discord.ext import commands as com
from discord import app_commands

from src.services.user_service import UserService
from src.services.wallet_service import WalletService
import src.utils.messages as message

user_service = UserService()
wallet_service = WalletService()

@com.hybrid_command('bytes', help="Consulte seu saldo de Bytes e ganhe um premio")
async def consulting_bytes(ctx: com.Context):
	try:
		msg = wallet_service.get_balance_wallet(ctx)
		await message.send_msg(ctx, msg, True)
	except Exception as e:
		raise e

def setup(bot):
	"""defina aqui os comandos no bot"""
	bot.add_command(consulting_bytes)
