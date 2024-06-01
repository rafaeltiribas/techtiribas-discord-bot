![image](https://github.com/rafaeltiribas/techtiribas-discord-bot/blob/main/assets/bot.png)

# TECHTIRIBAS BOT

## Objetivo
<hr>
O objetivo deste projeto é desenvolver um bot para a plataforma Discord com o objetivo de automatizar algumÍas ações dos usuários e adicionar algumas novas funcionalidades ao servidor. Além disso, ele poderá integrar-se com outras plataformas e APIs para expandir suas funcionalidades, tornando-se uma ferramenta versátil e útil para administradores e membros de servidores Discord.

## Funcionalidades
<hr>
Uma das funcionalidades esperadas que o bot realize é a de automatizar as notificações de lives e vídeos novos do canal TechTiribas na Twitch e Youtube. 

Outra ideia sugerida seria a de desenvolver um sistema monetário para o servidor, que conectado a uma API seja possível realizar apostas nos chats com uma moeda fictícia(Bytes).

Conforme o desenvolvimento do projeto, é esperado que novas funcionalidades venham surgindo e implementadas. Sendo assim, é de total incentivo novas sugestões e melhorias no código.

## Como executar o projeto
<hr>
Para executar o projeto, clone o repositório:

```bash
git clone https://github.com/rafaeltiribas/techtiribas-discord-bot.git && \
cd techtiribas-discord-bot
```

Crie um ambiente virtual:

```bash
python -m venv .venv && \
source .venv/bin/activate # ou .venv/Scripts/Activate se estiver no Windows
```

Instale as dependências:

```bash
pip install .[dev]
```

Copie o .env.example e coloque o seu token do discord conforme abaixo:

```
DISCORD_TOKEN="seu_token"
```

### Ferramentas úteis

Para ajudar no desenvolvimento aqui estao algumas automações:

```bash
task run # roda o script
task lint # roda o linter
task format # roda o formatador
```

## Estrutura Básica de código do Bot
<hr>

Como pode ver, na raiz do projeto voce encontra o ```main.py``` e o diretório ```src```

#### main.py

Onde se dá o "start" no bot, sincroniza os comandos, mostra mensagens de erro e inicia o ```src/commands.py``` com:
```python
commands.setup(bot)
```
#### o diretório ```src```

Onde fica localizado todo o restante do código, a partir daqui crie novas funcionalidades ou realize ajustes

#### commands.py
Onde se localiza a maioria dos comandos do bot.

Para criar novos comandos, use a anotação
```python
@com.hybrid_command(help="mensagem de descrição do comando")
async def nome_do_comando(ctx: com.Context):
```

depois adicione o mesmo em:

```python
def setup(bot):
    bot.add_command(nome_do_comando) # <-- preencha nos parenteses o nome do def do comando
```

## Por fim

Esse projeto será realizado ao vivo na Twitch(canal: TechTiribas) e em parceria com os membros do servidor do Discord.

## [Entre no nosso Discord](https://discord.gg/WWPT2xYczy)

