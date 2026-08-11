import asyncio
import datetime
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


_startup_announced = False


async def announce_startup():
    """Post a one-off "bot is up" notice, mirroring the vps-monitoring bot.

    on_ready fires again on every gateway reconnect, so the flag keeps a flaky
    connection from spamming the channel.
    """
    global _startup_announced
    if _startup_announced or config.DISCORD_CHANNEL_ID is None:
        return
    _startup_announced = True

    embed = discord.Embed(
        title='\U0001F535 bariola started',
        description='Deployment succeeded and the bot is now online.',
        colour=0x3498DB,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
    )
    embed.add_field(name='Version', value=config.APP_VERSION, inline=True)
    embed.add_field(name='Servers', value=str(len(bot.guilds)), inline=True)
    embed.set_footer(text='bariola')

    try:
        channel = bot.get_channel(int(config.DISCORD_CHANNEL_ID))
        if channel is None:
            channel = await bot.fetch_channel(int(config.DISCORD_CHANNEL_ID))
        await channel.send(embed=embed)
    except (discord.HTTPException, ValueError) as exc:
        print(f'Startup notice not sent: {exc}')


@bot.event
async def on_ready():
    change_status.start()
    print('I\'m ready!')
    await announce_startup()


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
