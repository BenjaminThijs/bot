import json
from discord.ext import commands


class Cog(commands.Cog):
    def __init__(self):
        with open("settings.json", "r") as settings_file:
            self.settings = json.load(settings_file)

    def save_settings(self):
        with open("settings.json", "w") as settings_file:
            json.dump(self.settings, settings_file, indent=4)
