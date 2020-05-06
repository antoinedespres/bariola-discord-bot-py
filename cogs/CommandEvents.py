from discord.ext import commands


class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Commande inexistante !')
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send('Il manque un ou plusieurs arguments :pouting_cat: !')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " appelée avec succès.")


def setup(bot):
    bot.add_cog(CommandEvents(bot))
