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
		msg = f'Saldo em Bytes: B$ {user_wallet.balance}.'
		
		interacted = self.user_inter_service.has_already_interacted(user)
		if not interacted:
			user_wallet.balance += 50.0
			msg += f'\nHoje você ganhou B$ 50,00 por interagir e ainda ganhará mais!'
			self.user_inter_service.add_user(user)
		
		con.commit()
		return msg