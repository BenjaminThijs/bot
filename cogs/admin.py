from cogs import cog
from discord.ext import commands


class Admin(cog.Cog):

    @commands.group(name="monitor", aliases=["watch"], brief="Monitor the users of a server")
    async def monitor(self, ctx):
        if ctx.invoked_subcommand is None:
            # No subcommand is entered, so we show the help info
            # Doing the help info through a send so we can access the prefix variable
            await ctx.send(
                "**Monitor / Watch**\n\nMonitor allows me to view who is a member of the server.\n" +
                "I will periodically check this information, this allows me to tell you when a person has left the server.\n\n" +
                f"If you want me to monitor this server, use the command `{ctx.prefix}monitor start`\n" +
                f"If you want me to stop monitoring this server, use the command `{ctx.prefix}monitor stop`\n" +
                f"If you want me to give you the latest changes to the server, use the command `{ctx.prefix}monitor status`"
            )
        elif ctx.guild is None:
            # A subcommand has been entered, but the message was not sent in a guild
            await ctx.send("This command can only be used in a server")
    
    @monitor.command(name="start", brief="Start monitoring this server")
    @cog.is_guild_owner()
    async def monitor_start(self, ctx):
        # We only care about the id of the server
        guild_id = ctx.guild.id

        if guild_id in self.settings["monitor"]:
            # The server is already in our list to be monitored
            await ctx.send("I'm already monitoring this server!")
        else:
            # Add the server to the list to be monitored
            self.settings["monitor"].append(guild_id)
            self.save_settings()

            await ctx.send(f"I'm now monitoring `{ctx.guild.name}`!")

            # Stqrt the monitor loop in cqse its not running yet
            if not self.monitor_loop.is_running():
                self.monitor_loop.start()

    @monitor.command(name="stop", brief="Stop monitoring this server")
    @cog.is_guild_owner()
    async def monitor_stop(self, ctx):
        # We only care about the id of the server
        guild_id = ctx.guild.id

        if not guild_id in self.settings["monitor"]:
            # This server is not in our list of monitored servers
            await ctx.send("I'm not monitoring this server")
        else:
            # Remove the server from the list to be monitored
            self.settings["monitor"].remove(guild_id)
            self.save_settings()

            await ctx.send(f"I have stopped monitoring `{ctx.guild.name}`")

            # NOTE: do we check if the loop is running here? Should be since something is still being monitored.
            # Stop the loop if no servers are left to be monitored
            if len(self.settings["monitor"]) == 0:
                self.monitor_loop.stop()

    @monitor.command(name="status", brief="Show the latest changes on this server")
    @cog.is_guild_owner()
    async def monitor_status(self, ctx):
        await ctx.send("Work in progress :)")
