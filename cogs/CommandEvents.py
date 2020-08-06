from discord.ext import commands


class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('Command does not exist!')
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('One or several arguments missing :pouting_cat:!')

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " successfully called.")


def setup(bot):
    bot.add_cog(CommandEvents(bot))
