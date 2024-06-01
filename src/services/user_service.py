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
	
	
	"""
		Para realizar a alteração da Role de um User, o User solicitante (ou seja, o que escreve o comando)
			deve ter uma Role maior e deve redesignar apenas para Roles menores, Ex:
			
			Usuario solicitante é um Admin, ele pode alterar uma Role de um User apenas para
				Subscriber ou Member.
			O solicitante é um Council , então pode alterar para Admin, Subscriber e Member
	"""
	def update_user_role(self, ctx, at_sign_user: str, role: str):
		"""Valida se a Role existe registrada"""
		if not User.is_valid_role(role):
			return f'Função {role} não é válida.'
		
		"""Valida se usuário marcado existe"""
		usr_updt = self.get_user_from_at_sign(at_sign_user)
		if usr_updt is None:
			return f'Usuário {at_sign_user} não encontrado!'
		
		requesting_user = self.get_user_by_ctx(ctx)
		
		if usr_updt.id_discord == requesting_user.id_discord:
			return "Você não pode alterar a sua própria função!"
		
		comparison = self.compare_hieranchy(requesting_user, usr_updt)
		
		"""Valida se o Usuario que gerou o comando tem Role maior ao que vai alterar"""
		if comparison < 0:
			return "Você não tem autorização para alterar função deste usuário"
		
		try:
			con = db.open_transaction()
			usr_updated = self.update_user(usr_updt, role)
			con.commit()
			return f'Usuario {usr_updated.username} atualizado com sucesso!'
		except Exception as e:
			con.rollback()
			return f'Não foi possível alterar o Usuário @<{usr_updt.id_discord}>. Fale com os Adm'
		
	def add_user(self, id_discord, username, role):
		role_str = ','.join(role)
		user = User(id_discord=id_discord, username=username, role=role_str)
		return user
	
	def update_user(self, user, new_role):
		if user is None:
			raise ValueError(f"Usuário não encontrado!")
		
		if not User.is_valid_role(new_role):
			raise ValueError(f"Função '{new_role}' não é válida")
		
		user.role = ','.join(User.ROLE[new_role])
		
		return user
	
	def create_wallet_for_user(self, user, balance=300.0):
		wallet = Wallet(user=user, balance=balance)
		TransactionHistory(wallet=wallet, value=balance, type_transaction=TransactionType.START.name, description="Start new register")
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
	
	def compare_hieranchy(self, user1, user2):
		hierarchy1 = User.HIERARCHY.get(user1.role, 0)
		hierarchy2 = User.HIERARCHY.get(user2.role, 0)
		return hierarchy1 - hierarchy2