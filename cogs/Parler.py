import random
from discord.ext import commands


class Parler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Miaou, {0.mention} !'.format(member))

    @commands.command(aliases=['miauler', 'meow'])
    async def miaou(self, ctx):
        miaous = ['Miaouuu :smiley_cat:', 'Miaou !', 'Miaouuuu (j\'ai faim !)', 'Miaou :heart_eyes_cat:', 'Zzzz...']
        await ctx.send(f'{random.choice(miaous)}')

    @commands.command(aliases=['infos', 'author'])
    async def about(self, ctx):
        await ctx.send('J\'ai été créée par Antoine Després, un étudiant en 1re année de DUT Informatique !'
                       '\nRegarde ses autres créations sur : https://github.com/antoinedespres')

    @commands.command(aliases=['answer', 'reponds', 'réponds'])
    async def question(self, ctx, *, question):
        responses = ['Tu rêves...',
                     'C\'est sûr !',
                     'Oui',
                     'Bien sûr !'
                     'T\'es pas mieux qu\'une sardine !',
                     'Non.',
                     'Arrête tes bêtises et vas bosser !',
                     'Absolument pas',
                     'Évidemment !',
                     'Peut-être, peut-être pas',
                     'M\'en fous j\'ai faim moi.',
                     'FAKE NEWS!',
                     'Je sais pas, je ne suis qu\'un chat.']

        await ctx.send(f'Question : {question}\n\nRéponse : {random.choice(responses)}')

    @commands.command(aliases=['manger', 'bouffe'])
    async def nourrir(self, ctx):
        reponsesnourrir = ['C\'était pas bon grrrr :pouting_cat:',
                           'Miam ! :joy_cat:',
                           'Mouais, ça remplit juste...',
                           'J\'aime bien :smile_cat: !'
                           'Délicieux :kissing_cat: !']
        await ctx.send(f'Mon avis : {random.choice(reponsesnourrir)}')

    @commands.command()
    async def cute(self, ctx):
        responses = ['T\'es trop sympa !',
                     'T\'es le meilleur !',
                     'T\'es trop mimi !',
                     'Tu as des qualités que les autres n\'ont pas !',
                     'T\'as trop la classe !',
                     'T\'es plus bo qu\'Anicet tkt\n(et si t\'es Anicet bah... désolé)']

        await ctx.send(f'{random.choice(responses)}')

    @commands.command(aliases=['funfact', 'apprendsmoi'])
    async def fact(self, ctx):
        facts = ['Nous les chats on passe 70 % de nos journées à dormir et 15 % à faire notre toilette !',
                 'Notre ouïe est cinq fois plus développée que celle de l\'humain !',
                 'Les motifs sur notre museau sont uniques, comme des empreintes digitales humaines !',
                 'Un chat peut sauter à une altitude représentant jusqu\'à 5 fois sa hauteur !',
                 'Les chats ne sont pas les seuls à ronronner ! Les éléphants aussi...',
                 'Les chats sont capables de boire de l\'eau de mer (nos reins sont trop forts !) !']

        await ctx.send(f'{random.choice(facts)}')

    @commands.command(aliases=['rrr', 'ronronner'])
    async def caresser(self, ctx):
        await ctx.send('Rrrrr !! :smile_cat:')

    @commands.command()
    async def random(self, ctx, nb1, nb2):
        result = random.randrange(int(nb1), (int(nb2) + 1), 1)
        await ctx.send(f'Résultat : {result}')


def setup(bot):
    bot.add_cog(Parler(bot))
