import discord
import os

from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix='.')
client.remove_command('help')

status = cycle(['manger des croquettes',
                'faire ses griffes',
                'faire la sieste',
                'espionner son maître',
                'regarder la télé',
                'miauler',
                'ne rien faire'])


@client.event
async def on_ready():
    change_status.start()
    print('Le bot est prêt.')


async def on_message(self, message):
    if message.author.bot:
        return  # ignore messages from other bots

    if message.author.id in self.blacklisted_users:
        return

    if message.guild is None:
        return  # ignore private messages


@tasks.loop(minutes=15)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong ! J\'ai réagi en {round(client.latency * 1000)} ms')


extensions = ['cogs.CommandEvents', 'cogs.HelpCommands', 'cogs.Parler']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

client.run(os.environ['TOKEN'])
