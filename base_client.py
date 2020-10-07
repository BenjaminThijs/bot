import json
import discord

class BaseClient(discord.Client):
    def __init__(self):
        super().__init__()

        with open("settings.json", "r") as settings:
            self.settings = json.load(settings)

        self.prefix = self.settings["prefix"]

        with open("commands.json", "r") as commands_json:
            self.commands = json.load(commands_json)

    def save_settings(self):
        with open("settings.json", "w") as settings:
            json.dump(settings, self.settings)

    async def say(self, channel, msg):
        await channel.send(msg)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author != self.user and message.content.startswith(self.prefix):
            # We called a command and didnt come from this bot

            # Get the command itself and the arguments given
            command_string, *args = message.content.split(' ')

            # Remove the prefix from the command
            command_string = command_string[1:]

            # First we need to find the actual command name (they might have used an alias)
            if not command_string in self.commands.keys():
                # They might have given an alias
                for c in self.commands.keys():
                    if command_string in self.commands[c]["aliases"]:
                        command_string = c
                        break
                else:
                    # They didnt give an alias
                    await self.say(message.channel, f"There is no command by that name: `{command_string}`")
                    return

            command = getattr(self, command_string)
                
            try:
                await command(message, *args)
            except:
                await self.say(message.channel, f"Something went wrong while running the command: `{command_string}`")
                return