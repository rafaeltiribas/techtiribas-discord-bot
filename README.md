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

Onde se dá o "start" no bot, sincroniza os comandos, mostra mensagens de erro e inicia o ```src/commands/commands.py``` com:
```python
commands.setup(bot)
```
Não só eles mas os outros comandos também, todos os .py que finalizam com ```_commands.py```
#### o diretório ```src```

Onde fica localizado todo o restante do código, a partir daqui crie novas funcionalidades ou realize ajustes

#### commands.py
Onde se localiza a maioria dos comandos do bot. Mas há outros ```_commands.py``` , estão localizados em ```src/commands/``` e funcionam do mesmo jeito.

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

## Bot Bank

O bot contém um "banco" no qual de acordo com um cron expression, ele executa um aumento percentual em todas as carteiras dos usuários. Algo
como se fosse um "CDB" .

#### Transferencias entre Usuários

O ```user``` consegue transferir para outro ```user``` uma quantidade de bytes, o bot valida se os dois ```users``` existem, se o saldo de bytes é maior que o solicitado para transferencia e até se a transferencia não é para ele mesmo. 

O comando atualmente é **/transferir_bytes** onde o user deve preencher marcando o user que vai receber a transferencia e o valor em bytes que será transferido.

Cheque o ```src/services/wallet_service.py``` no def ```transferir_bytes_para``` para entender melhor.

#### Jobs executados de acordo com Cron expressions
Como citado antes, o bot usa ```cron expressions``` para executar uma tarefa. Existe um service chamado ```jobs_service.py``` que cuida disso.

#### Wallets 
Cada ```user``` contém uma ```wallet``` (carteira) onde é armazenado o valor em bytes do usuário. Existe um comando **/bytes** que mostra o saldo

## Embed messages

O bot é capaz de mandar embed messages, que são aquelas mensagens destacadas que contém uma barra colorida na lateral esquerda da mesma. O ```messages.py``` é o responsável por criar e enviar essas mensagens.

Para entender melhor, busque pelo comando **/bytes** por exemplo, para ver como ele funciona ;)

## Por fim

Esse projeto será realizado ao vivo na Twitch(canal: TechTiribas) e em parceria com os membros do servidor do Discord.

## [Entre no nosso Discord](https://discord.gg/WWPT2xYczy)

