from src.models.user import User, Role
from src.models.wallet import Wallet
from src.exceptions.bot_errors import UserError, AdminError
from src.models.transaction_history import TransactionHistory, TransactionType
import src.functionalities.log as LOG
import db.database_config as db


class UserService:
		
		def register_user_from_ctx(self, ctx):
				con = db.open_transaction()
				try:
						if self.get_user_by_ctx(ctx) is not None:
								raise UserError('Você já está cadastrado! use **/** para ver outros comandos')
						
						user = self.save_user(str(ctx.author.id), ctx.author.name)
						wallet = self.create_wallet_for_user(user)
						con.commit()
						return f'Você foi Resgistrado! agora você possui uma carteira com {wallet.balance} Bytes!'
				except UserError as e:
						LOG.error("Houve erro ao cadastrar novo user: " + e.mensagem)
						con.rollback()
						raise e
		
		"""
			Para realizar a alteração da Role de um User, o User solicitante (ou seja, o que escreve o comando)
				deve ter uma Role maior e deve redesignar apenas para Roles menores, Ex:
				
				Usuario solicitante é um Admin, ele pode alterar uma Role de um User apenas para
					Subscriber ou Member.
				O solicitante é um Council , então pode alterar para Admin, Subscriber e Member
		"""
		
		def update_user_role(self, interaction, at_sign_user: str, role: str):
				role = role.capitalize()
				"""Valida se a Role existe registrada"""
				if not Role.is_valid(role):
						raise UserError(f'Função {role} não é válida.')
				
				"""Valida se usuário marcado existe"""
				usr_updt = self.get_user_from_at_sign(at_sign_user)
				if usr_updt is None:
						raise UserError(f'Usuário {at_sign_user} não encontrado!')
				
				requesting_user = self.get_user_from_interaction(interaction)
				
				if usr_updt.id_discord == requesting_user.id_discord:
						raise UserError("Você não pode alterar a sua própria função!")
				
				comparison = User.compare_roles(requesting_user.role, usr_updt.role)
				
				"""Valida se o Usuario que gerou o comando tem Role maior ao que vai alterar"""
				if "council" not in requesting_user.role.split(','):
						if comparison < 0:
								raise AdminError("Você não tem autorização para alterar função deste usuário")
						
						compare_future_role = User.compare_roles(requesting_user.role, role)
						if compare_future_role <= 0:
								raise UserError("Você não pode alterar para uma Função maior ou igual a sua!")
				
				try:
						con = db.open_transaction()
						usr_updated = self.update_user(usr_updt, role)
						con.commit()
						return f'Usuario {usr_updated.username} atualizado com sucesso!'
				except ValueError as ve:
						con.rollback()
						raise UserError(ve)
				except Exception as e:
						con.rollback()
						raise AdminError(f'Não foi possível alterar o Usuário {usr_updt.username}. Fale com os Adm')
		
		def save_user(self, id_discord, username):
				user = User(id_discord=id_discord, username=username, role=Role.Member.name)
				return user
		
		def update_user(self, user, new_role):
				if user is None:
						raise ValueError(f'Usuário não encontrado!')
				
				if not Role.is_valid(new_role):
						raise ValueError(f'Função {new_role} não é válida')
				
				user.role = Role[new_role].name
				return user
		
		def create_wallet_for_user(self, user, balance=300.0):
				wallet = Wallet(user=user, balance=balance)
				TransactionHistory(wallet=wallet, value=balance, type_transaction=TransactionType.START.name,
				                   description="Start new register")
				return wallet
		
		def get_user_by_ctx(self, ctx):
				return self.get_user_by_discord_id(str(ctx.author.id))
		
		def get_user_by_username(self, username):
				return User.selectBy(username=username).getOne(None)
		
		def get_user_from_at_sign(self, at_sign_user):
				dc_id = at_sign_user.replace('<', '').replace('>', '').replace('@', '')
				return self.get_user_by_discord_id(dc_id)
		
		def get_user_by_discord_id(self, id_discord):
				return User.selectBy(id_discord=id_discord).getOne(None)
		
		def get_user_from_interaction(self, interaction):
				return self.get_user_by_discord_id(str(interaction.user.id))
		
		def user_is_admin_or_higher(self, interaction) -> bool:
				user = self.get_user_from_interaction(interaction)
				if user is not None:
						valid =  Role.__getitem__(user.role).value >= Role.Admin.value
						# LOG.text_highlighted(f"Usuario tem a role {user.role}. Ele é maior ou igual a Admin? {valid}")
						return valid
				else:
						return False
