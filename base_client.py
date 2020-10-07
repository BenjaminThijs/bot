import json
import discord

class BaseClient(discord.Client):
    def __init__(self):
        super().__init__()

        with open("settings.json", "r") as settings:
            _settings = json.load(settings)

        self.prefix = _settings["prefix"]

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

            try:
                command = getattr(self, command_string)
            except:
                await self.say(message.channel, f"There is no command by that name: `{command_string}`")
                return
                
            try:
                await command(message, *args)
            except:
                await self.say(message.channel, f"Something went wrong while running the command: `{command_string}`")
                return