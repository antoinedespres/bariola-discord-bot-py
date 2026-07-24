import discord
from discord import app_commands
from discord.ext import commands

import i18n

NUMBER_EMOJIS = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
MIN_OPTIONS = 2
MAX_OPTIONS = len(NUMBER_EMOJIS)


class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Start a poll with up to 10 options.")
    @app_commands.describe(
        question="The question to ask.",
        options="The choices, separated by commas (2 to 10).",
    )
    async def poll(self, ctx, question: str, *, options: str):
        choices = [choice.strip() for choice in options.split(',') if choice.strip()]

        if not MIN_OPTIONS <= len(choices) <= MAX_OPTIONS:
            await ctx.send(await i18n.t_ctx(ctx, 'poll.invalid_options'))
            return

        description = '\n'.join(
            f'{NUMBER_EMOJIS[i]} {choice}' for i, choice in enumerate(choices)
        )
        embed = discord.Embed(title=question, description=description, colour=discord.Colour.dark_orange())

        message = await ctx.send(embed=embed)
        for i in range(len(choices)):
            await message.add_reaction(NUMBER_EMOJIS[i])


async def setup(bot):
    await bot.add_cog(Polls(bot))
