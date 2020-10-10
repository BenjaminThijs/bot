import json
import os
import time

from discord.ext import commands, tasks


class Cog(commands.Cog):
    def __init__(self, bot):
        with open("settings.json", "r") as settings_file:
            self.settings = json.load(settings_file)

        self.bot = bot

    def save_settings(self):
        # This will update the settings file to be the same as self.settings
        # This is an override so some settings might get lost
        # TODO: do some backup thing here?
        with open("settings.json", "w") as settings_file:
            json.dump(self.settings, settings_file, indent=4)

    # This code will run once every hour (if something needs to be monitored)
    @tasks.loop(hours=1)
    async def monitor_loop(self):
        print(f"Starting monitor cycle {self.monitor_loop.current_loop} at {time.ctime(time.time())}")

        for guild_id in self.settings["monitor"]:
            # Get the actual guild from the id
            # TODO: what if the bot got removed from a server it should be monitoring?
            guild = await self.bot.fetch_guild(guild_id)

            print(f"Starting monitoring cycle for server {guild.name} at {time.ctime(time.time())}")

            # This folder is where the files for this server will be stored
            # NOTE: we make the foldername both the id and the name, this way it is both readable for a user and still based on id
            folder = f"monitor/{guild_id}_{guild.name}"

            # Make sure we have a folder in which we can put the info for this server
            os.makedirs(folder, exist_ok=True)

            # Save the info we just retrieved into a json file
            # The json filename will be timebased to ensure no duplicates and the proper order
            with open(f"{folder}/{time.time_ns()}.json", "w") as monitor_file:
                # Get all the members on the server
                # We don't need all the info that is provided by the api
                json.dump([
                    {
                        "id": m.id,
                        "roles": [{"role_id": r.id, "role": r.name} for r in m.roles if not r.name == "@everyone"],
                        "display_name": m.display_name,
                        "nickname": m.nick
                    } async for m in guild.fetch_members()],
                    monitor_file, indent=4)

        print(f"Finished monitor cycle {self.monitor_loop.current_loop} at {time.ctime(time.time())}")

        # TODO: also monitor the audit logs?
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
