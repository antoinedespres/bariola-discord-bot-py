from discord.ext import commands

import i18n


class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(await i18n.t('greetings.member_join', member.guild.id, mention=member.mention))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(await i18n.t('greetings.member_remove', member.guild.id, mention=member.mention))


async def setup(bot):
    await bot.add_cog(Greetings(bot))
