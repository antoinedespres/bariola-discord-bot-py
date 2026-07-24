import asyncio
from itertools import cycle

import discord
from discord.ext import commands, tasks

import config
import db
import i18n

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix=config.BOT_PREFIX, intents=intents)
bot.remove_command('help')

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


@bot.event
async def on_ready():
    change_status.start()
    print('I\'m ready!')


@tasks.loop(minutes=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(game)), status=next(status))


@bot.hybrid_command(description="Check Bariola's latency.")
async def ping(ctx):
    await ctx.send(await i18n.t_ctx(ctx, 'bot.ping.response', latency=round(bot.latency * 1000)))


@bot.hybrid_command(description="Mention everyone in your current voice channel.")
async def vc(ctx):
    if ctx.author.voice is None:
        await ctx.send(await i18n.t_ctx(ctx, 'bot.vc.not_in_voice'))
        return

    for member in ctx.author.voice.channel.members:
        await ctx.send(member.mention)


@bot.command()
@commands.is_owner()
async def sync(ctx, scope: str = None):
    if scope == 'global':
        synced = await bot.tree.sync()
        await ctx.send(f'Synced {len(synced)} command(s) globally.')
        return

    if config.DEV_GUILD_ID is None:
        await ctx.send('DEV_GUILD_ID is not set — cannot sync to a dev guild.')
        return

    guild = discord.Object(id=int(config.DEV_GUILD_ID))
    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync(guild=guild)
    await ctx.send(f'Synced {len(synced)} command(s) to the dev guild.')


extensions = [
    'cogs.command_events',
    'cogs.greetings',
    'cogs.misc',
    'cogs.server_management',
    'cogs.talk',
    'cogs.language',
    'cogs.cat',
    'cogs.polls',
    'cogs.birthday',
]


async def load_extensions():
    for ext in extensions:
        await bot.load_extension(ext)


async def main():
    await db.init_db()
    try:
        async with bot:
            await load_extensions()
            await bot.start(config.BOT_TOKEN)
    finally:
        await db.close_db()


if __name__ == '__main__':
    asyncio.run(main())
