import discord
import os

from discord.ext import commands, tasks
from itertools import cycle

# Set up intents (required for discord.py 2.x)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

client = commands.Bot(command_prefix=os.environ['BOT_PREFIX_PY'], intents=intents)
client.remove_command('help')

game = cycle(['eating kibbles',
              'drinking water',
              'walking around',
              'sleeping',
              'scratching the couch',
              'napping',
              'spying on its owner',
              'watching TV',
              'meowing',
              'doing nothing',
              'walking on the keyboard',
              'talking with cats outside'])

status = cycle([discord.Status.dnd,
                discord.Status.online,
                discord.Status.idle,
                discord.Status.idle,
                discord.Status.online,
                discord.Status.idle,
                discord.Status.online,
                discord.Status.dnd,
                discord.Status.online,
                discord.Status.online,
                discord.Status.online,
                discord.Status.idle])


@client.event
async def on_ready():
    change_status.start()
    print('I\'m ready!')


async def on_message(self, message):
    if message.author.bot:
        return  # ignore messages from other bots

    if message.author.id in self.blacklisted_users:
        return  # ignore message from blacklisted users

    if message.guild is None:
        return  # ignore private messages


@tasks.loop(minutes=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(game)), status=next(status))


@client.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! I reacted in {round(client.latency * 1000)} ms.')


@client.command()
async def vc(ctx):
    channel = ctx.author.voice.channel

    if channel is not None:
        for member in channel.members:
            await ctx.send(member.mention)


extensions = ['cogs.CommandEvents', 'cogs.Greetings', 'cogs.HelpCommands', 'cogs.ServerMgmt', 'cogs.Talk', 'cogs.Music']

async def load_extensions():
    for ext in extensions:
        await client.load_extension(ext)

async def main():
    async with client:
        await load_extensions()
        await client.start(os.environ['BOT_TOKEN_PY'])

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
