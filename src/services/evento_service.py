import discord
import math
import db.database_config as db

from src.models.evento import Evento, Category, BettingHistory
from src.services.user_service import UserService
from src.services.wallet_service import WalletService
from src.exceptions.bot_errors import UserError

user_service = UserService()
wallet_service = WalletService()

class EventoService:
		
		def create_event(self, interaction: discord.Interaction, title: str, category: str, option_a: str, option_b: str):
				user = user_service.get_user_from_interaction(interaction)
				evt = Evento(title=title, category=category, option_a=option_a, option_b=option_b, user_who_started=user,
				             status='CRIADA')
				return evt
		
		def get_event_to_announce(self, interaction: discord.Interaction, id) -> Evento:
				user = user_service.get_user_from_interaction(interaction)
				if user is None:
						raise UserError(f"Não sei quem é tu... se cadastra aí com **/register**")
				
				if id <= 0:
						raise UserError(f"HÃN??? QUE EVENTO DE ID {id} É ESSE ??? EXISTE??")
				
				evento = Evento.selectBy(id=id).getOne(None)
				if evento is None:
						raise UserError(f"HÃN??? QUE EVENTO DE ID {id} É ESSE ??? EXISTE??")
				
				return evento
				
		def betting_on(self, interaction: discord.Interaction, id, opcao, bytes) -> dict:
				
				if bytes <= 0:
						raise UserError(f"me explica COMO QUE VOCE VAI APOSTAR B$ {bytes} ????")
				if opcao != "A" and opcao != "B":
						raise UserError("Vai apostar em quem ???? Escolha A ou B")
				if id <= 0:
						raise UserError(f"HÃN??? QUE EVENTO DE ID {id} É ESSE ??? EXISTE??")
				
				evento = Evento.selectBy(id=id).getOne(None)
				if evento is None:
						raise UserError(f"Voce sabia que o evento ID {id} NÃO EXISTE??? Tente apostar em outro")
				if evento.status == "FECHADA" or evento.status == "APOSTAS ENCERRADAS":
						raise UserError(f"Então, não dá pra apostar mais no evento '{evento.title}', não tem como!")
				
				user = user_service.get_user_from_interaction(interaction)
				if user is None:
						raise UserError(f"Não sei quem é tu... se cadastra aí com **/register**")
				
				option_selected = self._get_name_option(opcao, evento)
				
				con = db.open_transaction()  # Abrir uma transação para caso dê erro dar um rollback
				
				bet = BettingHistory.selectBy(user_who_bet=user).getOne(None)
				if bet is not None:
						raise UserError(f"Você já fez sua fézinha de B$ {bet.amount_bet} no {option_selected}")
				
				wallet = wallet_service.get_user_wallet(user)
				if bytes > wallet.balance:
						raise UserError(f"VOCÊ TÁ POBRE!! Você não tem bytes suficientes para realizar aposta no valor B$ {bytes}")
				
				if opcao == "A":
						evento.total_amount_a += round(bytes, 2)
				else:
						evento.total_amount_b += round(bytes, 2)
				
				wallet.balance -= bytes
				
				self._calculate_odds(evento)
				
				BettingHistory(user_who_bet=user, evento=evento, amount_bet=bytes, option_selected=option_selected)
				
				evento.status = "APOSTAS ABERTAS"
				
				con.commit()
				
				return {
						"Valor apostado:": {"value": f"B$ {round(bytes, 2)}", "inline": True},
						"Apostou no:": {"value": option_selected, "inline": True}
				}
		
		def _smooth_probability(self, bytes):
				return math.log(bytes + 1, 10)
		
		def _calculate_odds(self, evento: Evento):
				if evento.total_amount_a != 0.0:
						odds_a = ((self._smooth_probability(evento.total_amount_b)) / (
								self._smooth_probability(evento.total_amount_a))) + 1
						evento.odds_a = round(odds_a, 2)
				if evento.total_amount_b != 0.0:
						odds_b = ((self._smooth_probability(evento.total_amount_a)) / (
								self._smooth_probability(evento.total_amount_b))) + 1
						evento.odds_b = round(odds_b, 2)
		
		def _get_name_option(self, option: str, evento: Evento) -> str:
				if option == "A":
						return evento.option_a
				else:
						return evento.option_b
