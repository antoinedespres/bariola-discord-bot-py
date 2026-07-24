import datetime

from discord import app_commands
from discord.ext import commands, tasks

import db
import i18n


class Birthday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start()

    def cog_unload(self):
        self.check_birthdays.cancel()

    @commands.hybrid_command(description="Set your birthday; Bariola will wish you a happy birthday on the day!")
    @commands.guild_only()
    @app_commands.describe(day="Day of the month (1-31)", month="Month (1-12)")
    async def birthday(self, ctx, day: int, month: int):
        try:
            datetime.date(2000, month, day)  # 2000 is a leap year, so Feb 29 validates too
        except ValueError:
            await ctx.send(await i18n.t_ctx(ctx, 'birthday.invalid_date'))
            return

        await db.set_birthday(ctx.guild.id, ctx.author.id, day, month)
        await ctx.send(await i18n.t_ctx(ctx, 'birthday.set_confirmation', day=day, month=month))

    @tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
    async def check_birthdays(self):
        today = datetime.datetime.now(datetime.timezone.utc)
        rows = await db.get_birthdays_on(today.day, today.month)

        for guild_id, user_id in rows:
            guild = self.bot.get_guild(guild_id)
            if guild is None or guild.system_channel is None:
                continue

            member = guild.get_member(user_id)
            mention = member.mention if member is not None else f'<@{user_id}>'
            await guild.system_channel.send(
                await i18n.t('birthday.announcement', guild_id, mention=mention)
            )

    @check_birthdays.before_loop
    async def before_check_birthdays(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Birthday(bot))
