import json
from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self, bot):
        with open("settings.json", "r") as settings_file:
            self.settings = json.load(settings_file)

        self.bot = bot

    def save_settings(self):
        with open("settings.json", "w") as settings_file:
            json.dump(self.settings, settings_file, indent=4)

def is_guild_owner():
    # TODO: silent failure?

    # You need to be owner of the guild (or the bot)
    async def predicate(ctx):
        if await ctx.bot.is_owner(ctx.author) or ctx.guild.owner_id == ctx.author.id:
            return True

        await ctx.send("You need to be owner of the server or the bot to use this command")

    return commands.check(predicate)
