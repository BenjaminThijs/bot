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
                f"If you want me to monitor this server, use the command `{ctx.prefix}monitor start` in the channel where you want me to log.\n" +
                f"If you want me to stop monitoring this server, use the command `{ctx.prefix}monitor stop` anywhere in the server."
            )
        elif ctx.guild is None:
            # A subcommand has been entered, but the message was not sent in a guild
            await ctx.send("This command can only be used in a server")
    
    @monitor.command(name="start", brief="Start monitoring this server")
    @cog.is_guild_owner()
    async def monitor_start(self, ctx):
        # We only care about the id of the server and channel
        guild_id = ctx.guild.id
        channel_id = ctx.channel.id

        if guild_id in self.bot.watcher.keys():
            # The server is already in our list to be monitored
            await ctx.send("I'm already monitoring this server!")
        else:
            # Add the server to the list to be monitored
            self.bot.watcher[str(guild_id)] = channel_id
            self.bot.save_watcher()

            await ctx.send(f"I'm now monitoring `{ctx.guild.name}`!")

    @monitor.command(name="stop", brief="Stop monitoring this server")
    @cog.is_guild_owner()
    async def monitor_stop(self, ctx):
        # We only care about the id of the server
        guild_id = ctx.guild.id

        if not guild_id in self.bot.watcher.keys():
            # This server is not in our list of monitored servers
            await ctx.send("I'm not monitoring this server")
        else:
            # Remove the server from the list to be monitored
            self.bot.watcher.pop(guild_id)
            self.bot.save_watcher()

            await ctx.send(f"I have stopped monitoring `{ctx.guild.name}`")

    @commands.command(name="stop", aliases=["exit", "off"], brief="Turn off the bot")
    async def stop(self, ctx):
        await ctx.send("Bye bye")
        await self.bot.logout()

    @commands.command(name="reload", brief="Reload all cogs")
    async def reload(self, ctx):
        for c in list(self.bot.cogs):
            self.bot.remove_cog(c)

        for c in self.bot.cogs.all_cogs:
            self.bot.add_cog(eval(c)(self.bot))

        await ctx.send("Done reloading")

    @commands.command(name="test", brief="Nobody knows if this command will even work")
    async def test(self, ctx):
        print("-----------------------------------------")
        print(str(self.bot.intents))
        ctx.guild.intents
