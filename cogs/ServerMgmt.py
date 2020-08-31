import json

import discord
from discord.ext import commands

warnings = {}


class ServerMgmt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    with open('warnings.json', 'r') as infile:
        warnings = json.load(infile)

    # warning and auto-kick
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warning(self, ctx, warnedMember: discord.Member):
        pseudo = warnedMember.mention
        memberID = warnedMember.id

        if memberID not in warnings:
            warnings[memberID] = 0
            print("This member has no warning")

        warnings[memberID] += 1
        print("Added warning", warnings[memberID], "/3")

        if warnings[memberID] == 3:
            warnings[memberID] = 0
            await warnedMember.send(
                "You have been kicked of the server because of too many warnings. Meow :pouting_cat:!")
            await warnedMember.kick()

        with open('warnings.json', 'w') as outfile:
            json.dump(warnings, outfile)

        await ctx.send(f"Member {pseudo} has received a warning! Beware :pouting_cat:!")

    @warning.error
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message):
        # TODO Remove user's message
        await ctx.send(message)


def setup(bot):
    bot.add_cog(ServerMgmt(bot))
