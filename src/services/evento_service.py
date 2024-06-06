import discord
import math
import db.database_config as db
import src.utils.messages as message

from src.models.evento import Evento, Category, BettingHistory, BettingPayments
from src.models.wallet import Wallet
from datetime import datetime
from src.services.user_service import UserService
from src.services.wallet_service import WalletService
from src.exceptions.bot_errors import UserError
import src.utils.log as LOG

user_service = UserService()
wallet_service = WalletService()


class EventoService:
		
		def create_event(self, interaction: discord.Interaction, title: str, category: str, option_a: str, option_b: str):
				user = user_service.get_user_from_interaction(interaction)
				evt = Evento(title=title.upper(), category=category, option_a=option_a, option_b=option_b, user_who_started=user,
				             status='CRIADA')
				return evt
		
		def close_bets(self, interaction: discord.Interaction, id: int):
				evento = Evento.selectBy(id=id).getOne(None)
				if evento is None:
						raise UserError(f"HÃN??? QUE EVENTO DE ID {id} É ESSE ??? EXISTE??")
				if evento.status == "APOSTAS ENCERRADAS":
						raise UserError(f"Já foi encerrado as apostas bonitão...")
				
				user = user_service.get_user_from_interaction(interaction)
				if evento.user_who_started != user:
						raise UserError("Você não pode encerrar evento dos outros ¬¬")
				
				evento.status = "APOSTAS ENCERRADAS"
				return self._create_msg_close_bets(evento)
		
		def finalize_events(self, interaction: discord.Interaction, id: int, vencedor: str):
				evento = Evento.selectBy(id=id).getOne(None)
				if evento is None:
						raise UserError(f"HÃN??? QUE EVENTO DE ID {id} É ESSE ??? EXISTE??")
				if evento.status == "FECHADA":
						raise UserError(f"Esse evento já foi encerrado...")
				if evento.status != "APOSTAS ENCERRADAS":
						raise UserError(f"ENCERRE AS APOSTAS PRIMEIRO! INTELIJENTE")
				
				user = user_service.get_user_from_interaction(interaction)
				if evento.user_who_started != user:
						raise UserError("Você não pode encerrar evento dos outros ¬¬")
				
				con = db.open_transaction()
				
				if vencedor == "A":
						option_winner_name = evento.option_a
				else:
						option_winner_name = evento.option_b
						
				bettings_that_won = list(BettingHistory.selectBy(evento=evento, option_selected=option_winner_name))
				LOG.info_highlighted(f"Total de usuários vencedores no evento {evento.id} : {len(bettings_that_won)}")
				
				if vencedor == "A":
						odd_winner = evento.odds_a
				else:
						odd_winner = evento.odds_b
				
				winners = []
				for bet in bettings_that_won:
						wallet = wallet_service.get_user_wallet(bet.user_who_bet)
						value_won = bet.amount_bet * odd_winner
						wallet.balance += round(value_won, 2)
						winners.append(BettingPayments(user=bet.user_who_bet, evento=evento, value_won=round(value_won, 2)))
				
				evento.status = "FECHADA"
				evento.finalize_at = datetime.now()
				evento.who_win = vencedor
				
				con.commit()
				
				# Generating a new embed message
				
				embed = message.gen_embed_message(
						title=f"OS GANHADORES DO EVENTO ID #{evento.id}",
						description="Só quem tá mandando agora papai... respeita",
						color = discord.Color.gold(),
						footer="Evento acabou! Tmj papai é nós!"
				)
				
				for win in winners:
						embed.add_field(name="Usuário", value=f"<@{win.user.id_discord}>", inline=True)
						embed.add_field(name="Ganhou B$", value=f"{win.value_won}", inline=True)
						
				return embed
				
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
				
				bet = BettingHistory.selectBy(user_who_bet=user, evento=evento).getOne(None)
				if bet is not None:
						raise UserError(f"Você já fez sua fézinha de B$ {bet.amount_bet} no {bet.option_selected}")
				
				wallet = wallet_service.get_user_wallet(user)
				if bytes > wallet.balance:
						raise UserError(f"VOCÊ TÁ POBRE!! Você não tem bytes suficientes para realizar aposta no valor B$ {bytes}")
				
				if opcao == "A":
						evento.total_bets_a += 1
						evento.total_amount_a += round(bytes, 2)
				else:
						evento.total_bets_b += 1
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
		
		
		def _create_msg_close_bets(self, evt: Evento):
				fields = {
						"Sobre apostas:" : {"value" : self._info_about_media_on_historic_values(evt), "inline": True},
						"Total de bets:" : {"value" : (evt.total_bets_a + evt.total_bets_b), "inline": True}
				}
				embed = message.gen_embed_message(
						title=f"ID[#{evt.id}] {evt.title}",
						description="APOSTAS ENCERRADAS!!!",
						color=discord.Color.orange(),
						fields=fields
				)
				return embed
		
		def _info_about_media_on_historic_values(self, evento: Evento) -> str:
				closed_events = list(Evento.selectBy(category=evento.category, status="FECHADA"))
				if closed_events is None or len(closed_events) == 0:
						return f"Ainda não há quantidade de apostas suficientes na categoria {evento.category} para obter informações"
				
				totals_history = 0.0
				for evt in closed_events:
						totals_history += (evt.total_amount_a + evt.total_amount_b)
				
				media_history = totals_history / len(closed_events)
				total_amount = (evento.total_amount_a + evento.total_amount_b)
				if media_history > total_amount:
						return f"Total de apostas foi abaixo da média para {evento.category}"
				elif total_amount > totals_history:
						return f"HISTÓRICO! Esse é o novo recorde de apostas na categoria {evento.category}"
				else:
						return f"Total de apostas foi acima da média para categoria {evento.category}"
				
				
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
