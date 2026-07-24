from discord.ext import commands

import i18n


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        aliases=['info', 'author', 'creator'],
        description="Some information about the creator of this bot and Bariola!",
    )
    async def about(self, ctx):
        await ctx.send(await i18n.t_ctx(ctx, 'misc.about'))


async def setup(bot):
    await bot.add_cog(Misc(bot))
