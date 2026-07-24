import aiohttp
from discord.ext import commands

import i18n

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"


class Cat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Get a random cat picture!")
    async def cat(self, ctx):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(CAT_API_URL) as response:
                    data = await response.json()
            image_url = data[0]['url']
        except (aiohttp.ClientError, KeyError, IndexError):
            await ctx.send(await i18n.t_ctx(ctx, 'cat.fetch_error'))
            return

        await ctx.send(image_url)


async def setup(bot):
    await bot.add_cog(Cat(bot))
