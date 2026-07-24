import discord
from discord.ext import commands

import db
import i18n

WARNING_KICK_THRESHOLD = 3


class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Warn a member; auto-kicks after 3 warnings.")
    @commands.has_permissions(administrator=True)
    async def warning(self, ctx, warned_member: discord.Member):
        count = await db.increment_warning(ctx.guild.id, warned_member.id)

        if count >= WARNING_KICK_THRESHOLD:
            await db.reset_warnings(ctx.guild.id, warned_member.id)
            await warned_member.send(await i18n.t_ctx(ctx, 'servermanagement.warning.kicked'))
            await warned_member.kick()

        await ctx.send(await i18n.t_ctx(ctx, 'servermanagement.warning.issued', mention=warned_member.mention))

    @warning.error
    async def warning_error(self, ctx, error):
        await ctx.send(await i18n.t_ctx(ctx, 'servermanagement.warning.bad_argument'))

    @commands.hybrid_command(description="Kick a member from the server.")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member_to_kick: discord.Member):
        await member_to_kick.send(await i18n.t_ctx(ctx, 'servermanagement.kick.notice'))
        await member_to_kick.kick()

    @commands.hybrid_command(description="Ban a member from the server.")
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member_to_ban: discord.Member):
        await member_to_ban.send(await i18n.t_ctx(ctx, 'servermanagement.ban.notice'))
        await member_to_ban.ban()

    @commands.hybrid_command(description="Bulk-delete messages from this channel.")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int = 5):
        await ctx.channel.purge(limit=amount)

    @commands.hybrid_command(description="Have Bariola repeat a message (admin-only).")
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message: str):
        if ctx.interaction is None:
            await ctx.channel.purge(limit=1)  # Removes the message which called the command
        await ctx.send(message)

    @commands.hybrid_command(description="Show a member's avatar.")
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
        await ctx.send(member.display_avatar.url)


async def setup(bot):
    await bot.add_cog(ServerManagement(bot))
