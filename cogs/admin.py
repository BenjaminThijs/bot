from cogs.cog import Cog
from discord.ext import commands


class Admin(Cog):

    @commands.command(name="monitor", aliases=["watch"])
    async def monitor(self, ctx, option=None):
        # TODO: check if owner
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server")
            return

        guild_id = ctx.guild.id

        if option is None:
            # No arguments were given, or not the correct ones
            await ctx.send_help('monitor')
            # await self.say(ctx.channel, 
            #     "**Monitor**\nMonitor allows me to view who is a member of the server.\n" +
            #     "I will periodically check this information, this allows me to tell you when a person has left the server.\n\n" +
            #     f"If you want me to monitor this server, use the command `{ctx.prefix}monitor start`\n" +
            #     f"If you want me to stop monitoring this server, use the command `{ctx.prefix}monitor stop`\n" +
            #     f"If you want me to give you the latest changes to the server, use the command `{ctx.prefix}monitor status`"
            # )

        elif option == "start":
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

        elif option == "stop":
            if not guild_id in self.settings["monitor"]:
                await ctx.send("I'm not monitoring this server")
            else:
                self.settings["monitor"].remove(guild_id)
                self.save_settings()

                await ctx.send(f"I have stopped monitoring `{ctx.guild.name}`")

                # TODO: potentially stop loop here

        elif option == "status":
            await ctx.send("Work in progress :)")
