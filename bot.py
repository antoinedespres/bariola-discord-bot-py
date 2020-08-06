import json
import discord
import os

from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix='$')
client.remove_command('help')

warnings = {}

with open('warnings.json', 'r') as infile:
    warnings = json.load(infile)

status = cycle(['eating kibbles',
                'drinking water',
                'walking around',
                'sleeping',
                'doing its claws',
                'napping',
                'spying on its owner',
                'watching TV',
                'meowing',
                'grooming',
                'doing nothing'])


@client.event
async def on_ready():
    change_status.start()
    print('I\'m ready!')


async def on_message(self, message):
    if message.author.bot:
        return  # ignore messages from other bots

    if message.author.id in self.blacklisted_users:
        return  # not yet implemented

    if message.guild is None:
        return  # ignore private messages


@tasks.loop(minutes=15)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


# warning and auto-kick
@client.command()
@commands.has_permissions(administrator=True)
async def warning(ctx, warnedMember: discord.Member):
    pseudo = warnedMember.mention
    memberID = warnedMember.id

    if memberID not in warnings:
        warnings[memberID] = 0
        print("This member has no warning")

    warnings[memberID] += 1
    print("Added warning", warnings[memberID], "/3")

    if warnings[memberID] == 3:
        warnings[memberID] = 0
        await warnedMember.send("You have been kicked of the server because of too many warnings. Meow :pouting_cat:!")
        await warnedMember.kick()

    with open('warnings.json', 'w') as outfile:
        json.dump(warnings, outfile)

    await ctx.send(f"Member {pseudo} has received a warning! Beware :pouting_cat:!")


@warning.error
async def on_command_error(ctx, error):
    await ctx.send(error)


@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
async def ping(ctx):
    await ctx.send(f':ping_pong: Pong! I reacted in {round(client.latency * 1000)} ms.')


extensions = ['cogs.CommandEvents', 'cogs.HelpCommands', 'cogs.Talk']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)

client.run(os.environ['BOT_TOKEN_PY'])
