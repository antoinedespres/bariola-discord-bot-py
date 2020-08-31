import discord
from discord.ext import commands


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.author

        embed = discord.Embed(
            colour=discord.Colour.dark_orange()
        )

        embed.set_author(name='What I can do')
        embed.add_field(name='$ping', value='Sends "Pong"!" with latency.', inline=False)
        embed.add_field(name='$meow', value='Meowww!', inline=False)
        embed.add_field(name='$random x y', value='Generates a random number between x and y inclusive.', inline=False)
        embed.add_field(name='$fact', value='Sends an interesting fact about cats.', inline=False)
        embed.add_field(name='$feed', value='I\'m hungry!!!', inline=False)
        embed.add_field(name='$question', value='I answer a closed question (Yes / No).', inline=False)
        embed.add_field(name='$cute', value='A kind phrase to cheer you up!', inline=False)
        embed.add_field(name='$notcute', value='An... unkind phrase.', inline=False)
        embed.add_field(name='$discord', value='Join the community on the official Bariola server!', inline=False)
        embed.add_field(name='$about', value='Some information about the creator of this bot and myself!', inline=False)
        embed.add_field(name='$say', value='I\'ll repeat what you wrote!', inline=False)

        await author.send(embed=embed)
        await ctx.send("PM sent :smile_cat:!")

    @commands.command(aliases=['info', 'author'])
    async def about(self, ctx):
        await ctx.send('I\'m Bariola, a four-year-old calico cat.'
                       'My name comes from the word "bariolé" (French) which means "coloured in bright and varied '
                       'tones".\n'
                       'The digital version of me was created by Antoine Després, a 1st year student'
                       ' of DUT diploma in Computer Science.'
                       '\nCheck out his other creations on:  https://github.com/antoinedespres')


def setup(bot):
    bot.add_cog(HelpCommands(bot))
