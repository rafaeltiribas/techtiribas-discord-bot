from src.services.user_service import UserService
from src.services.user_interactions_service import UserInteractionsService
from src.models.wallet import Wallet
from src.exceptions.bot_errors import UserError
import db.database_config as db
import locale

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')

class WalletService:
		user_service = UserService()
		user_inter_service = UserInteractionsService()
		
	
		def get_balance_wallet(self, interaction):
				con = db.open_transaction()
				user = self.user_service.get_user_from_interaction(interaction)
				if user == None:
						raise UserError("Você não está cadastrado, como que quer ter saldo de bytes???")
				
				user_wallet = Wallet.selectBy(user=user).getOne(None)
				msg = f'**B$ {self._format_float_to_money(user_wallet.balance)}**'
				
				interacted = self.user_inter_service.has_already_interacted(user)
				if not interacted:
						user_wallet.balance += 50.0
						msg += f'\nHoje você garantiu B$ 50,00 por interagir!'
						self.user_inter_service.add_user(user)
				
				con.commit()
				return msg
		
		def get_user_wallet(self, user) -> Wallet:
				return Wallet.selectBy(user=user).getOne(None)
			
		
		def transferir_bytes_para(self, interaction, username, value):
				if value == 0:
						raise UserError("COMO QUE VOCÊ VAI TRANSFERIR 0 BYTES ????")
				
				if value < 0:
						raise UserError(f"COMO QUE VOCÊ VAI TRANSFERIR B$ {value} NEGATIVOS ????")
				
				con = db.open_transaction()
				user = self.user_service.get_user_from_interaction(interaction)
				if user is None:
						con.rollback()
						raise UserError("Você não está cadastrado! Use **/register**")
				
				user_who_received = self.user_service.get_user_from_at_sign(username)
				if user_who_received is None:
						con.rollback()
						raise UserError(f"Usuário {username} não encontrado!")
				
				if user_who_received is user:
						con.rollback()
						raise UserError(f"Você não pode transferir para você mesmo! Troxa")
				
				user_wallet = Wallet.selectBy(user=user).getOne(None)
				if user_wallet.balance < float(value):
						con.rollback()
						raise UserError(f"Você não tem bytes suficientes para transferir B$ {self._format_float_to_money(value)}!")
				
				user_received_wallet = Wallet.selectBy(user=user_who_received).getOne(None)
				
				user_wallet.balance -= float(value)
				user_received_wallet.balance += float(value)
				
				con.commit()
				
				return f"Transferência de B$ {self._format_float_to_money(value)} realizada com sucesso!"

		def _format_float_to_money(self, value):
				return locale.currency(value, grouping=True).replace("R$ ", "")