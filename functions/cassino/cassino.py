import discord.ext.commands as command

class Cassino:

    @command('cassino', help='Cassinagem e malandragem')
    async def cassino(ctx):
        print(ctx)