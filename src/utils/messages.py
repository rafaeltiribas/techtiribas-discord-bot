import discord
import os
from typing import Dict, Optional


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


async def send_with_img(ctx, embed_message, img_name) -> None:
	img_path = os.path.abspath(f'assets/{img_name}')
	if os.path.isfile(img_path):
		with open(img_path, 'rb') as f:
			picture = discord.File(f, filename=img_name)
			embed_message.set_image(url=f"attachment://{img_name}")
			await ctx.author.send(embed=embed_message, file=picture)
	else:
		await ctx.author.send(embed=embed_message)
