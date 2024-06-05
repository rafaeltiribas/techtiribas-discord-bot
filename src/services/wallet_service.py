from src.services.user_service import UserService
from src.services.user_interactions_service import UserInteractionsService
from src.models.wallet import Wallet
import db.database_config as db


class WalletService:
	user_service = UserService()
	user_inter_service = UserInteractionsService()
	
	def get_balance_wallet(self, ctx):
		con = db.open_transaction()
		user = self.user_service.get_user_by_ctx(ctx)
		if user == None:
			raise "Usuário não cadastrado!"
		
		user_wallet = Wallet.selectBy(user=user).getOne(None)
		msg = f'B$ {user_wallet.balance}.'
		
		interacted = self.user_inter_service.has_already_interacted(user)
		if not interacted:
			user_wallet.balance += 50.0
			msg += f'\nHoje você garantiu B$ 50,00 por interagir!'
			self.user_inter_service.add_user(user)
		
		con.commit()
		return msg
	
	def transferir_bytes_para(self, ctx, username, value):
		con = db.open_transaction()
		user = self.user_service.get_user_by_ctx(ctx)
		if user is None:
			con.rollback()
			raise ValueError("Você não está cadastrado! Use **/register**")
		
		user_who_received = self.user_service.get_user_from_at_sign(username)
		if user_who_received is None:
			con.rollback()
			raise ValueError(f"Usuário {username} não encontrado!")
		
		if user_who_received is user:
			con.rollback()
			raise ValueError(f"Você não pode transferir para você mesmo! Troxa")
			
		user_wallet = Wallet.selectBy(user=user).getOne(None)
		if user_wallet.balance < float(value):
			con.rollback()
			raise ValueError(f"Você não tem bytes suficientes para transferir B$ {value}!")
		
		user_received_wallet = Wallet.selectBy(user=user_who_received).getOne(None)
		
		user_wallet.balance -= float(value)
		user_received_wallet.balance += float(value)
		
		con.commit()
		
		return f"Transferência de B$ {value} realizada com sucesso!"
		