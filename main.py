import os

from discord import Client, Intents, Message
from dotenv import find_dotenv, load_dotenv

from responses import get_response

# GET TOKEN
load_dotenv(find_dotenv('.venv/.env'))
TOKEN = os.getenv('DISCORD_TOKEN')

# Configurando as necessidades do bot: Ler e enviar mensagens
intests = Intents.default()
intests.message_content = True
client = Client(intents=intests)


# Funcionalidades de mensagem
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('Intents não foram configurados propriamente.')
        return

    # '?' é usado quando o usuário deseja receber a resposta no privado.
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response = get_response(user_message)
        await message.author.send(
            response
        ) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


# Manuseando a inicialização e funcionamento do Bot
@client.event
async def on_read() -> None:
    print(f'{client.user} está rodando')


@client.event
async def on_message(message: Message) -> None:
    # Verifica se o autor da mensagem é o próprio Bot
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    if user_message[0] == '=':
        print(f'[{channel}] {username}: "{user_message[1:]}"')
        await send_message(message, user_message[1:])


# Main  entry point
def main() -> None:
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
