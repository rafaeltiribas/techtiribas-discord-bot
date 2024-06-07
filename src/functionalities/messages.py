import discord
import os
import random
from typing import Dict, Optional
from src.functionalities.assets import Assets
from src.models.evento import Evento

gifs = Assets()

def gen_embed_message(
		title: str,
		description: str,
		color: discord.Color,
		fields: Optional[Dict[str, Dict[str, str]]] = None,
		author: Optional[Dict[str, str]] = None,
		footer: Optional[str] = None,
		url_img: Optional[str] = None
) -> discord.Embed:
		"""
		Gera uma mensagem embed para o Discord.
	
		Parameters:
		- title (str): O título do embed.
		- description (str): A descrição do embed.
		- color (discord.Color): A cor do embed.
		- fields (dict): Um dicionário de campos para adicionar ao embed, onde a chave é o nome do campo e o valor é outro dicionário com "value" e "inline".
		- author (dict): Um dicionário com informações do autor, contendo "name" e "icon_url".
		- footer (str): O texto do rodapé do embed.
		- url_img (str): A URL da imagem para definir no embed.
	
		Returns:
		- discord.Embed: O objeto embed configurado.
		"""
		
		embed_msg = discord.Embed(title=title, description=description, color=color)
		
		if author:
				embed_msg.set_author(name=author.get("name"), icon_url=author.get("icon_url"))
		
		if fields:
				for name, field in fields.items():
						embed_msg.add_field(name=name, value=field.get("value"), inline=field.get("inline", True))
		
		if footer:
				embed_msg.set_footer(text=footer)
		
		if url_img:
				embed_msg.set_image(url=url_img)
		
		return embed_msg

async def announce_event(interaction, evt: Evento):
		fields = {
				"Status do Evento:": {"value": f"{evt.status}", "inline": True},
				f"{evt.option_a}:": {"value": f"Odds: (x{evt.odds_a})", "inline": True},
				f"{evt.option_b}:": {"value": f"Odds: (x{evt.odds_b})", "inline": True},
		}
		desc = f'use **/evento apostar {evt.id}** para apostar!'
		if evt.status != "APOSTAS ABERTAS" and evt.status != "CRIADA":
				desc = "APOSTAS ENCERRADAS! Que vença o melhor!"
		
		embed = gen_embed_message(
				title=f"ID [#{evt.id}] - {evt.title}",
				description=desc,
				color=discord.Color.yellow(),
				fields=fields
		)
		await send_embed_with_img(interaction, embed, "evento", "category" ,f"{evt.category}", only_author_can_see=False)


async def send_user_error_msg(interaction, error, only_author_can_see=True):
		msg = gen_embed_message(mensagens_inspiradoras(), error, discord.Color.red(), footer=mensagens_inspiradoras())
		await send_embed_with_img(interaction, msg, "errors","user", only_author_can_see=only_author_can_see)


async def send_std_error_msg(interaction, error, only_author_can_see=True):
		msg = gen_embed_message("Ops! Aconteceu algo ruim...", error, discord.Color.red())
		await send_embed_with_img(interaction, msg, "errors","internal_error", only_author_can_see=only_author_can_see)


async def send_admin_error_msg(interaction, error, only_author_can_see=True):
		msg = gen_embed_message("Ops! Deu ruim ein...", error, discord.Color.red())
		await send_embed_with_img(interaction, msg, "errors", "admin", only_author_can_see=only_author_can_see)

async def send_embed_msg(interaction, embed_message, only_author_can_see=True):
		await interaction.response.send_message(embed=embed_message, ephemeral=only_author_can_see)


async def send_embed_with_img_to_ctx(ctx, embed_message, *path_nodes, only_author_can_see=True) -> None:
		picture = gifs.get_discord_file(path_nodes)
		embed_message.set_image(url=f"attachment://{picture.filename}")
		await ctx.send(embed=embed_message, file=picture, ephemeral=only_author_can_see)


async def send_embed_with_img(interaction, embed_message, *path_nodes, only_author_can_see=True) -> None:
		picture = gifs.get_discord_file(*path_nodes)
		embed_message.set_image(url=f"attachment://{picture.filename}")
		await interaction.response.send_message(embed=embed_message, file=picture, ephemeral=only_author_can_see)


async def send_msg_whom_interacted(interaction, msg, only_author_can_see=True) -> None:
		await interaction.response.send_message(msg, ephemeral=only_author_can_see)


async def send_msg_in_ctx(ctx, msg, only_author_can_see=False) -> None:
		await ctx.send(msg, ephemeral=only_author_can_see)


def mensagens_inspiradoras() -> str:
		frases = [
				"Tente novamente, campeão!",
				"Não foi dessa vez, hein?",
				"Voce é burro ou o que???",
				"Parece que hoje não é seu dia",
				"Não desista, perdedor!",
				"Talvez um dia você acerte.",
				"Isso é tudo que você tem?",
				"Foi por pouco... só que não!",
				"Quem sabe na próxima né? Nessa aqui você foi burro",
				"Você está quase lá... só que não!",
				"Persistência é a chave... ou não.",
				"Continue tentando, nunca vai dar certo",
				"De novo? Sério?",
				"Você está melhorando... MENTIRA!",
				"Mais uma tentativa frustrada, parabéns!",
				"Não desanime, só foi horrível sempre",
				"É, hoje não é seu dia de sorte...",
				"A sorte não está do seu lado NUNCA né?",
				"Quase... SQN!",
				"Ih, o que importa é competiiir...",
				"Você tentou, mas falhou denovo miseravelmente!",
				"A persistência é o caminho do fracasso, continue!",
				"Você vai chegar lá... mas acho que não",
				"Parabéns por tentar e errar... de novo."
		]
		
		return random.choice(frases)
