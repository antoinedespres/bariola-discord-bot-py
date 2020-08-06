import random
from discord.ext import commands


class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Meow, {0.mention} (welcome)!'.format(member))

    @commands.command(aliases=['meowing', 'miaou'])
    async def meow(self, ctx):
        meows = ['Meoowwww :smiley_cat:', 'Meow!', 'Meoooow (I\'m hungry!)', 'Meow :heart_eyes_cat:', 'Zzz...']
        await ctx.send(f'{random.choice(meows)}')

    @commands.command(aliases=['answer', 'ask', 'q'])
    async def question(self, ctx, *, question):
        answers = ['You\'re dreaming...',
                   'That\'s for sure.',
                   'Yes.',
                   'Of course!',
                   'Mais oui c\'est clair ! :flag_fr:',
                   'No.',
                   'Go back to work!',
                   'Absolutely not',
                   'Not at all.'
                   'Obviously!',
                   'Maybe, maybe not...',
                   'I don\'t care, I\'m hungry.',
                   'FAKE NEWS!',
                   'I don\'t know, I\'m just a cat.']

        await ctx.send(f'Your question: {question}\n\nMy answer: {random.choice(answers)}')

    @commands.command(aliases=['manger', 'nourrir'])
    async def feed(self, ctx):
        feed = ['That wasn\'t good :pouting_cat:',
                'Yum! :joy_cat:',
                'Meh, it just fills in...',
                'I like it :smile_cat:!',
                'Delicious :kissing_cat:!',
                'It\'s so good :heart_eyes_cat:!']
        await ctx.send(f'My opinion: {random.choice(feed)}')

    @commands.command()
    async def cute(self, ctx):
        cute = ['You\'re so nice!',
                'You\'re the best!',
                'You\'re so cute!',
                'You have qualities that others don\'t!',
                'You\'re so classy!']

        await ctx.send(f'{random.choice(cute)}')

    @commands.command()
    async def notcute(self, ctx):
        notcute = ['You\'re no better than a sardine!',
                   'You must be pretty bored to be talking to a cat on Discord...',
                   'Watch out, I claw!',
                   '*scratch* :pouting_cat:']

        await ctx.send(f'{random.choice(notcute)}')

    @commands.command(aliases=['funfact', 'learn'])
    async def fact(self, ctx):
        facts = ['We cats spend 70% of our days sleeping and 15% grooming!',
                 'Our hearing is five times more developed than that of humans!',
                 'The patterns on our snout are unique, like human fingerprints!',
                 'A cat can jump at an altitude of up to 5 times its height!',
                 'Cats aren\'t the only ones who purr! Elephants too...',
                 'Cats are able to drink sea water (our kidneys are so strong)!']

        await ctx.send(f'{random.choice(facts)}')

    @commands.command(aliases=['rrr', 'caresser'])
    async def cuddle(self, ctx):
        await ctx.send('Rrr! :smile_cat:')

    @commands.command()
    async def random(self, ctx, nb1, nb2):
        if nb1 < nb2:
            result = random.randrange(int(nb1), (int(nb2) + 1), 1)
        else:
            result = random.randrange(int(nb2), (int(nb1) + 1), 1)
        await ctx.send(f'Result: {result}')

    @commands.command()
    async def discord(self, ctx):
        await ctx.send('Join us! https://discord.gg/tzt7Gx2 :smile_cat:')


def setup(bot):
    bot.add_cog(Talk(bot))
