from cogs.cog import Cog
from discord.ext import commands


class Admin(Cog):

    @commands.group(name="monitor", aliases=["watch"], brief="Monitor the users of a server")
    async def monitor(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                "**Monitor / Watch**\n\nMonitor allows me to view who is a member of the server.\n" +
                "I will periodically check this information, this allows me to tell you when a person has left the server.\n\n" +
                f"If you want me to monitor this server, use the command `{ctx.prefix}monitor start`\n" +
                f"If you want me to stop monitoring this server, use the command `{ctx.prefix}monitor stop`\n" +
                f"If you want me to give you the latest changes to the server, use the command `{ctx.prefix}monitor status`"
            )
        elif ctx.guild is None:
            await ctx.send("This command can only be used in a server")
    
    @monitor.command(name="start", brief="Start monitoring this server")
    async def monitor_start(self, ctx):
        # TODO: check if owner
        guild_id = ctx.guild.id

        if guild_id in self.settings["monitor"]:
            await ctx.send("I'm already monitoring this server!")
        else:
            self.settings["monitor"].append(guild_id)
            self.save_settings()

            await ctx.send(f"I'm now monitoring `{ctx.guild.name}`!")

            # TODO: potentially start loop here
            # members = await guild.fetch_members(limit=150).flatten()
            # joined_at, id, roles, display_name
            # https://discordpy.readthedocs.io/en/latest/api.html?highlight=ctx#discord.Guild.audit_logs

    @monitor.command(name="stop", brief="Stop monitoring this server")
    async def monitor_stop(self, ctx):
        # TODO: check if owner
        guild_id = ctx.guild.id

        if not guild_id in self.settings["monitor"]:
            await ctx.send("I'm not monitoring this server")
        else:
            self.settings["monitor"].remove(guild_id)
            self.save_settings()

            await ctx.send(f"I have stopped monitoring `{ctx.guild.name}`")

            # TODO: potentially stop loop here

    @monitor.command(name="status", brief="Show the latest changes on this server")
    async def monitor_status(self, ctx):
        await ctx.send("Work in progress :)")
