import json
from discord.ext import commands, tasks


class Cog(commands.Cog):
    def __init__(self, bot):
        with open("settings.json", "r") as settings_file:
            self.settings = json.load(settings_file)

        self.bot = bot

    def save_settings(self):
        with open("settings.json", "w") as settings_file:
            json.dump(self.settings, settings_file, indent=4)

    @tasks.loop(seconds=10)
    async def monitor_loop(self):

        members = await guild.fetch_members(limit=150).flatten()
        # joined_at, id, roles, display_name
        # https://discordpy.readthedocs.io/en/latest/api.html?highlight=ctx#discord.Guild.audit_logs
        pass

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
