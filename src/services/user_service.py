from src.models.user import User
from src.models.wallet import Wallet
from src.models.transaction_history import TransactionHistory, TransactionType
import db.database_config as db
class UserService:

	def register_user_from_ctx(self, ctx):
		con = db.open_transaction()
		try:
			if self.get_user_by_ctx(ctx) is not None:
				return 'Você já está cadastrado! use **/** para ver outros comandos'
			user_id = str(ctx.author.id)
			username = ctx.author.name
			user = self.add_user(user_id, username, User.ROLE["Member"])
			wallet = self.create_wallet_for_user(user)
			con.commit()
			return f'Você foi Resgistrado! agora você possui uma carteira com {wallet.balance} Bytes!'
		except Exception as e:
			print("Houve erro ao cadastrar novo user: "+e)
			con.rollback()
			return e
		
	def add_user(self, id_discord, username, role):
		role_str = ','.join(role)
		user = User(id_discord=id_discord, username=username, role=role_str)
		return user
	
	def create_wallet_for_user(self, user, balance=300.0):
		wallet = Wallet(user=user, balance=balance)
		TransactionHistory(wallet=wallet, value=balance, type_transaction=TransactionType.START.name, description="Start new register")
		return wallet