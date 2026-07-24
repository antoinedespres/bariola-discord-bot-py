from typing import Literal

from discord.ext import commands

import db
import i18n


class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="language", description="Manage this server's language.")
    async def language(self, ctx):
        pass

    @language.command(name="set", description="Set the language Bariola replies in on this server.")
    @commands.has_permissions(administrator=True)
    async def language_set(self, ctx, language: Literal["en", "fr", "ko"]):
        await db.set_guild_language(ctx.guild.id, language)
        name = await i18n.t(f'language.name.{language}', ctx.guild.id)
        await ctx.send(await i18n.t('language.set_confirmation', ctx.guild.id, language=name))


async def setup(bot):
    await bot.add_cog(Language(bot))
