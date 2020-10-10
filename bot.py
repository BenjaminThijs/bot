from discord.ext import commands

import cogs


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with open("settings.json", "r") as settings_file:
            self.settings = json.load(settings_file)

        for c in cogs.all_cogs:
            self.add_cog(eval(c)(self))

    def save_settings(self):
        # This will update the settings file to be the same as self.settings
        # This is an override so some settings might get lost
        # TODO: do some backup thing here?
        with open("settings.json", "w") as settings_file:
            json.dump(self.settings, settings_file, indent=4)

    def can_check_guild(self, guild_id):
        # Is this guild part of the monitored list?
        return guild_id in self.settings["monitor"]

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        # Get the admin_cog
        admin_cog = self.get_cog("Admin")

        # The bot has just started up, we need to check if we need to start the monitor_loop
        if len(admin_cog.settings["monitor"]) > 0:
            print(f"Starting monitoring loop")
            admin_cog.monitor_loop.start()

    # MESSAGES
    async def on_message_delete(self, message):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(message.guild.id):
            return

    async def on_message_edit(self, before, after):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(before.guild.id):
            return

    # MEMBERS
    async def on_member_join(self, member):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(member.guild.id):
            return

    async def on_member_remove(self, member):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(member.guild.id):
            return

    async def on_member_update(self, before, after):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(before.guild.id):
            return

    # BANS
    async def on_member_ban(self, guild, user):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(guild.id):
            return

    async def on_member_unban(self, guild, user):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(guild.id):
            return

    # ROLES
    async def on_guild_role_create(self, role):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(role.guild.id):
            return

    async def on_guild_role_delete(self, role):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(role.guild.id):
            return

    async def on_guild_role_update(self, before, after):
        # If the guild is not in the monitored list we shouldn't catch this event
        if not self.can_check_guild(before.guild.id):
            return    
