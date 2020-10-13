import os
import json
import datetime

import discord
from discord import Embed, Color
from discord.ext import commands

import cogs


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            with open("monitor.json", "r") as monitor_file:
                self.watcher = json.load(monitor_file)
        except:
            # json doesnt exist
            self.watcher = {}
            self.save_watcher()

        for c in cogs.all_cogs:
            self.add_cog(eval(c)(self))

    def save_watcher(self):
        # This will update the monitor file to be the same as self.watcher
        # This is an override so some monitor might get lost
        # TODO: do some backup thing here?
        with open("monitor.json", "w") as monitor_file:
            json.dump(self.watcher, monitor_file, indent=4)

    def can_check_guild(self, guild):
        # Is this guild part of the monitored list?
        return self.watcher.get(str(guild.id), None)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    # Watcher logging method
    async def log(self, guild, embed):
        # If the author is the bot, ignore it
        # If this message doesnt come from a guild, ignore it
        # If the guild is not in the monitored list we shouldn't log anything
        if embed.author == str(self.user) or guild is None or (channel_id := self.can_check_guild(guild)) is None:
            return

        # We need to retrieve the channel from the id first
        channel = await self.fetch_channel(channel_id)

        # Send the log
        await channel.send(
            embed=embed
        )

    # MESSAGES
    # TODO: what to do with files?
    async def on_message_delete(self, message):
        await self.log(
            guild=message.guild,
            embed=Embed(
                description=message.content,
                color=Color.red()
            ).set_author(
                name=str(message.author)
            ).set_footer(
                text="deleted"
            )
        )

    async def on_message_edit(self, before, after):
        try:
            await self.log(
                guild=before.guild,
                embed=Embed(
                    color=Color.orange()
                ).set_author(
                    name=str(before.author)
                ).add_field(
                    name="Before",
                    value=before.content
                ).add_field(
                    name="After",
                    value=after.content
                ).set_footer(
                    text="edited"
                )
            )
        except discord.errors.HTTPException:
            # Not sure why this keeps getting thrown, something to do with the add_fields
            # The code still works though
            r"""
            Ignoring exception in on_message_edit
            Traceback (most recent call last):
            File "C:\Users\flopown\AppData\Local\Programs\Python\Python39\lib\site-packages\discord\client.py", line 333, in _run_event
                await coro(*args, **kwargs)
            File "D:\mass\projects\bot\bot.py", line 67, in on_message_edit
                await self.log(
            File "D:\mass\projects\bot\bot.py", line 47, in log
                await channel.send(
            File "C:\Users\flopown\AppData\Local\Programs\Python\Python39\lib\site-packages\discord\abc.py", line 904, in send
                data = await state.http.send_message(channel.id, content, tts=tts, embed=embed,
            File "C:\Users\flopown\AppData\Local\Programs\Python\Python39\lib\site-packages\discord\http.py", line 245, in request
                raise HTTPException(r, data)
            discord.errors.HTTPException: 400 Bad Request (error code: 50035): Invalid Form Body
            In embed.fields.0.value: This field is required
            In embed.fields.1.value: This field is required
            """
            pass

    # MEMBERS
    async def on_member_join(self, member):
        await self.log(
            guild=member.guild,
            embed=Embed(
                color=Color.green()
            ).set_author(
                name=str(member)
            ).set_footer(
                text="joined"
            )
        )

    async def on_member_remove(self, member):
        await self.log(
            guild=member.guild,
            embed=Embed(
                color=Color.red()
            ).set_author(
                name=str(member)
            ).set_footer(
                text="left / kicked"
            )
        )

    async def on_member_update(self, before, after):
        pass

    # BANS
    async def on_member_ban(self, guild, user):
        await self.log(
            guild=guild,
            embed=Embed(
                color=Color.red()
            ).set_author(
                name=str(user)
            ).set_footer(
                text="banned"
            )
        )

    async def on_member_unban(self, guild, user):
        await self.log(
            guild=guild,
            embed=Embed(
                color=Color.green()
            ).set_author(
                name=str(user)
            ).set_footer(
                text="unbanned"
            )
        )

    # ROLES
    async def on_guild_role_create(self, role):
        await self.log(
            guild=role.guild,
            embed=Embed(
                description=role.name,
                color=Color.green()
            ).set_footer(
                text="role added"
            )
        )

    async def on_guild_role_delete(self, role):
        await self.log(
            guild=role.guild,
            embed=Embed(
                description=role.name,
                color=Color.red()
            ).set_footer(
                text="role deleted"
            )
        )

    async def on_guild_role_update(self, before, after):
        pass 
