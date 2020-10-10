import json
import os
import time

from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def is_guild_owner():
    # You need to be owner of the guild (or the bot owner)
    async def predicate(ctx):
        if await ctx.bot.is_owner(ctx.author) or ctx.guild.owner_id == ctx.author.id:
            return True

        await ctx.send("You need to be owner of the server or the bot to use this command")
        # If the code reaches this point then an error will be raised by the internal code from commands.check()
        # TODO: silent failure?
        pass

    return commands.check(predicate)
