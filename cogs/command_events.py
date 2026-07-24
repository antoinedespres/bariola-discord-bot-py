from discord.ext import commands

import i18n


class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(await i18n.t_ctx(ctx, 'commandevents.command_not_found'))
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(await i18n.t_ctx(ctx, 'commandevents.missing_argument'))

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        print(ctx.command.name + " successfully called by " + str(ctx.author))


async def setup(bot):
    await bot.add_cog(CommandEvents(bot))
