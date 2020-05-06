import discord
from discord.ext import commands


class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.author

        embed = discord.Embed(
            colour=discord.Colour.dark_orange()
        )

        embed.set_author(name='Ce que je sais faire')
        embed.add_field(name='.ping', value='Renvoie « Pong ! » avec le temps de latence.', inline=False)
        embed.add_field(name='.miaou', value='Miaouuu !', inline=False)
        embed.add_field(name='.random x y', value='Génère un nombre aléatoire entre x et y inclus.', inline=False)
        embed.add_field(name='.fact', value='Envoie un fait intéressant sur les chats.', inline=False)
        embed.add_field(name='.nourrir', value='Pour me donner à manger !.', inline=False)
        embed.add_field(name='.question', value='Je réponds à une question fermée (Oui / Non).', inline=False)
        embed.add_field(name='.cute', value='Une phrase gentille pour te réconforter !', inline=False)
        embed.add_field(name='.cute', value='Une phrase... pas gentille.', inline=False)
        embed.add_field(name='.about', value='Quelques infos sur le créateur de ce bot et moi-même !', inline=False)

        await author.send(embed=embed)
        await ctx.send("MP envoyé :smile_cat: !")

    @commands.command(aliases=['infos', 'author'])
    async def about(self, ctx):
        await ctx.send('Je suis Bariola, une chatte calico âgée de 4 ans. '
                       'Mon nom vient du mot « bariolé » qui signifie « coloré de tons vifs et variés ».\n'
                       'La version numérique de ma personne a été créée par Antoine Després, un étudiant en 1re année '
                       'de DUT Informatique ! '
                       '\nRegarde ses autres créations sur : https://github.com/antoinedespres')


def setup(bot):
    bot.add_cog(HelpCommands(bot))
