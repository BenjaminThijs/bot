from base_client import BaseClient

class Client(BaseClient):
    """
        To add a command, create an async method here which takes a `message` and some `*args`.
        Add the methodname to the commands.json file as a new key, this needs to be an object which contains an entry for `aliases`.
    """

    async def stop(self, message, *args):
        await self.say(message.channel, "Bye bye")
        await self.close()

    async def monitor(self, message, *args):
        # TODO: check if owner
        guild_id = message.guild.id

        if not args:
            # No arguments were given, or not the correct ones
            await self.say(message.channel, 
                "**Monitor**\nMonitor allows me to view who is a member of the server.\n" +
                "I will periodically check this information, this allows me to tell you when a person has left the server.\n\n" +
                f"If you want me to monitor this server, use the command `{self.prefix}monitor start`\n" +
                f"If you want me to stop monitoring this server, use the command `{self.prefix}monitor stop`\n" +
                f"If you want me to give you the latest changes to the server, use the command `{self.prefix}monitor status`"
            )

        elif args[0] == "start":
            if guild_id in self.settings["monitor"]:
                await self.say(message.channel, "I'm already monitoring this server")
            else:
                self.settings["monitor"].append(guild_id)
                self.save_settings()

                await self.say(message.channel, f"I'm now monitoring `{message.guild.name}`!")

                # TODO: potentially start loop here
                # members = await guild.fetch_members(limit=150).flatten()
                # joined_at, id, roles, display_name
                # https://discordpy.readthedocs.io/en/latest/api.html?highlight=message#discord.Guild.audit_logs

        elif args[0] == "stop":
            if not guild_id in self.settings["monitor"]:
                await self.say(message.channel, "I'm not monitoring this server")
            else:
                self.settings["monitor"].remove(guild_id)
                self.save_settings()

                await self.say(message.channel, f"I have stopped monitoring `{message.guild.name}`")

                # TODO: potentially stop loop here

        elif args[0] == "status":
            await self.say(message.channel, "Work in progress :)")
