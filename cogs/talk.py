import random

from discord.ext import commands

import i18n

MEOW_COUNT = 5
QUESTION_ANSWER_COUNT = 13
FEED_COUNT = 6
CUTE_COUNT = 5
NOTCUTE_COUNT = 4
FACT_COUNT = 6


class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases=['meowing', 'miaou'], description="Meow!")
    async def meow(self, ctx):
        index = random.randrange(MEOW_COUNT)
        await ctx.send(await i18n.t_ctx(ctx, f'talk.meow.{index}'))

    @commands.hybrid_command(aliases=['answer', 'ask', 'q'], description="Ask Bariola a closed (yes/no) question.")
    async def question(self, ctx, *, question: str):
        index = random.randrange(QUESTION_ANSWER_COUNT)
        answer = await i18n.t_ctx(ctx, f'talk.question.{index}')
        await ctx.send(await i18n.t_ctx(ctx, 'talk.question.prefix', question=question, answer=answer))

    @commands.hybrid_command(aliases=['manger', 'nourrir'], description="Feed Bariola!")
    async def feed(self, ctx):
        index = random.randrange(FEED_COUNT)
        opinion = await i18n.t_ctx(ctx, f'talk.feed.{index}')
        await ctx.send(await i18n.t_ctx(ctx, 'talk.feed.prefix', opinion=opinion))

    @commands.hybrid_command(description="Get a kind phrase to cheer you up.")
    async def cute(self, ctx):
        index = random.randrange(CUTE_COUNT)
        await ctx.send(await i18n.t_ctx(ctx, f'talk.cute.{index}'))

    @commands.hybrid_command(description="Get an... unkind phrase.")
    async def notcute(self, ctx):
        index = random.randrange(NOTCUTE_COUNT)
        await ctx.send(await i18n.t_ctx(ctx, f'talk.notcute.{index}'))

    @commands.hybrid_command(aliases=['funfact', 'learn'], description="Get an interesting fact about cats.")
    async def fact(self, ctx):
        index = random.randrange(FACT_COUNT)
        await ctx.send(await i18n.t_ctx(ctx, f'talk.fact.{index}'))

    @commands.hybrid_command(aliases=['rrr', 'caresser'], description="Cuddle Bariola!")
    async def cuddle(self, ctx):
        await ctx.send(await i18n.t_ctx(ctx, 'talk.cuddle.response'))

    @commands.hybrid_command(description="Generate a random number between two bounds, inclusive.")
    async def randint(self, ctx, nb1: int, nb2: int):
        low, high = sorted((nb1, nb2))
        result = random.randint(low, high)
        await ctx.send(await i18n.t_ctx(ctx, 'talk.randint.result', result=result))

    @commands.hybrid_command(name='discord', description="Join the official Bariola community server!")
    async def discord_invite(self, ctx):
        await ctx.send(await i18n.t_ctx(ctx, 'talk.discord.invite'))


async def setup(bot):
    await bot.add_cog(Talk(bot))
