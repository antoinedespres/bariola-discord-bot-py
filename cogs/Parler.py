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
        await ctx.send('Je suis Bariola, une chatte calico âgée de 4 ans. '
                       'Mon nom vient du mot « bariolé » qui signifie « coloré de tons vifs et variés ».\n'
                       'La version numérique de ma personne a été créée par Antoine Després, un étudiant en 1re année '
                       'de DUT Informatique ! '
                       '\nRegarde ses autres créations sur : https://github.com/antoinedespres')

    @commands.command(aliases=['answer', 'reponds', 'réponds'])
    async def question(self, ctx, *, question):
        responses = ['Tu rêves...',
                     'C\'est sûr !',
                     'Oui.',
                     'Bien sûr !',
                     'Mais oui c\'est clair !',
                     'Non.',
                     'Arrête tes bêtises et vas bosser !',
                     'Absolument pas',
                     'Pas du tout'
                     'Évidemment !',
                     'Peut-être, peut-être pas...',
                     'M\'en fous j\'ai faim moi.',
                     'FAKE NEWS!',
                     'Je sais pas, je ne suis qu\'un chat.']

        await ctx.send(f'Question : {question}\n\nRéponse : {random.choice(responses)}')

    @commands.command(aliases=['manger', 'feed', 'bouffer'])
    async def nourrir(self, ctx):
        nourrir = ['C\'était pas bon grrrr :pouting_cat:',
                   'Miam ! :joy_cat:',
                   'Mouais, ça remplit juste...',
                   'J\'aime bien :smile_cat: !',
                   'Délicieux :kissing_cat: !',
                   'Cest trop bon :heart_eyes_cat: !']
        await ctx.send(f'Mon avis : {random.choice(nourrir)}')

    @commands.command()
    async def cute(self, ctx):
        cute = ['T\'es trop sympa !',
                'T\'es le meilleur !',
                'T\'es trop mimi !',
                'Tu as des qualités que les autres n\'ont pas !',
                'T\'as trop la classe !',
                'T\'es plus bo qu\'Anicet tkt\n(et si t\'es Anicet bah... désolé)']

        await ctx.send(f'{random.choice(cute)}')

    @commands.command()
    async def notcute(self, ctx):
        notcute = ['T\'es pas mieux qu\'une sardine !',
                   'Tu dois bien t\'ennuyer pour parler à un chat sur Discord...',
                   'Attention, je griffe !',
                   '*coup de griffe* :pouting_cat:']

        await ctx.send(f'{random.choice(notcute)}')

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
