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

    # command to warn someone in case of bad behavior. In case of 3 warnings,
    # the person is kicked from the server
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warning(self, ctx, warned_member: discord.Member):
        pseudo = warned_member.mention
        member_id = warned_member.id

        if member_id not in warnings:
            warnings[member_id] = 0
            print("This member has no warning")

        warnings[member_id] += 1
        print("Added warning", warnings[member_id], "/3")

        if warnings[member_id] == 3:
            warnings[member_id] = 0
            await warned_member.send(
                "You have been kicked of the server because of too many warnings. Meow :pouting_cat:!")
            await warned_member.kick()

        with open('warnings.json', 'w') as outfile:
            json.dump(warnings, outfile)

        await ctx.send(f"Member {pseudo} has received a warning! Beware :pouting_cat:!")

    @warning.error
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member_to_kick: discord.Member):
        await member_to_kick.send(
            "It's bad to be bad! :pouting_cat:")
        await member_to_kick.kick()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member_to_ban: discord.Member):
        await member_to_ban.send(
            "It's bad to be bad! :pouting_cat:")
        await member_to_ban.ban()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message):

        await ctx.channel.purge(limit=1)  # Removes the message which called the command
        await ctx.send(message)

    @commands.command()
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.send(member.display_avatar.url)


async def setup(bot):
    await bot.add_cog(ServerMgmt(bot))
