import os
import json
import datetime
import asyncio

import discord
from discord import Embed, Color, AuditLogAction
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

    async def send(self, channel, embed):
        # Send the embed
        await channel.send(
            embed=embed
        )

    # Watcher logging method
    async def log(self, guild, embed):
        # If the author is the bot, ignore it
        # If this message doesnt come from a guild, ignore it
        # If the guild is not in the monitored list we shouldn't log anything
        if guild is None or (channel_id := self.can_check_guild(guild)) is None:
            return

        # We need to retrieve the channel from the id first
        channel = await self.fetch_channel(channel_id)

        await self.send(channel, embed)

    # MESSAGES
    async def on_message_delete(self, message):
        # TODO: what to do with files?
        # If the message was sent by the bot, or is in the channel where we are logging, ignore
        if message.author == self.user or message.channel.id == self.can_check_guild(message.guild):
            return

        # TODO: to check if someone else removed the message you need to retrieve the audit-logs
        # NOTE: The problem here is that the entry.created_at doesnt change even if a second message from the same user gets removed by the same user in the same channel
        # NOTE: the only thing that changes in the entry is the entry.extra.count, but the only way we can use this is by keeping track of this count in memory.
        # NOTE: this makes it so that we basically have to check all this stuff ourselves, so ye, skip that for now

        await self.log(
            guild=message.guild,
            embed=Embed(
                description=message.content,
                color=Color.red()
            ).set_author(
                name=str(message.author)
            ).set_footer(
                text="deleted their own message"
            )
        )

    async def on_message_edit(self, before, after):
        # If the message was sent by the bot, or is in the channel where we are logging, ignore
        if before.author == self.user or before.channel.id == self.can_check_guild(before.guild):
            return

        # It is possible for an edit to have occured without a change in content
        # This happens when the user shares a link for instance, since discord then edits the message to show a preview
        if before.content == after.content:
            return

        await self.log(
            guild=before.guild,
            embed=Embed(
                color=Color.orange()
            ).set_author(
                name=str(before.author)
            ).add_field(
                name="before",
                value=before.content
            ).add_field(
                name="after",
                value=after.content
            ).set_footer(
                text="edited"
            )
        )

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
        # TODO: this also triggers on ban
        # TODO: what if we arent allowed to see audit logs
        # NOTE: we assume the event always gets called before the audit logs get updated
        trigger_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)

        # Give Discord some time to put the potential kick in the audit logs
        await asyncio.sleep(1)

        # Check all kicks after this event was triggered
        async for entry in member.guild.audit_logs(action=AuditLogAction.kick):
            # NOTE: the `after`-tag in audit_logs seems to get ignored :|, so we have to check manually
            if trigger_time > entry.created_at:
                # No entry was found mentioning this kick
                # The member was not kicked, they left
                await self.log(
                    guild=member.guild,
                    embed=Embed(
                        color=Color.red()
                    ).set_author(
                        name=str(member)
                    ).set_footer(
                        text="left the server"
                    )
                )
                break

            elif entry.target == member:
                # Check if the target is the member that left
                # They got kicked
                await self.log(
                    guild=member.guild,
                    embed=Embed(
                        color=Color.red()
                    ).set_author(
                        name=str(entry.user)
                    ).add_field(
                        name="kicked",
                        value=str(member)
                    ).add_field(
                        name="reason",
                        value=entry.reason
                    )
                )
                break

    async def on_member_update(self, before, after):
        def _role_change(before, after):
            before = [b.name for b in before]
            after = [a.name for a in after]

            if (role := _role_added(before, after)):
                return "added", role
            elif (role := _role_removed(before, after)):
                return "removed", role    

        def _role_added(before, after):
            for role in after:
                if role not in before:
                    return role

        def _role_removed(before, after):
            for role in before:
                if role not in after:
                    return role

        # Called when one of the following has changed: status, activity, nickname, roles
        # We only care about nickname or role changes
        if before.nick == after.nick and (action_role := _role_change(before.roles, after.roles)) is None:
            return

        # Nickname change
        if before.nick != after.nick:
            await self.log(
                guild=before.guild,
                embed=Embed(
                    color=Color.orange()
                ).set_author(
                    name=str(before)
                ).add_field(
                    name="before",
                    value=before.nick
                ).add_field(
                    name="after",
                    value=after.nick
                ).set_footer(
                    text="changed nickname"
                )
            )

        # NOTE: I really wish they added unpacking to walrus
        if action_role:
            action, role = action_role

            await self.log(
                guild=before.guild,
                embed=Embed(
                    color=Color.green() if action == "added" else Color.red(),
                    description=role
                ).set_author(
                    name=str(before)
                ).set_footer(
                    text="role " + action
                )
            )

    # BANS
    async def on_member_ban(self, guild, user):
        # TODO: what if we arent allowed to see audit logs
        # NOTE: we assume the event always gets called before the audit logs get updated
        trigger_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)

        # Give Discord some time to put the ban in the audit logs
        await asyncio.sleep(1)

        # Only check bans and after the time this event got triggered
        async for entry in guild.audit_logs(action=AuditLogAction.ban):
            # NOTE: the `after`-tag in audit_logs seems to get ignored :|, so we have to check manually
            if trigger_time > entry.created_at:
                await self.log(
                    guild=guild,
                    embed=Embed(
                        color=Color.purple(),
                        description="Ban happened, but audit logs dont seem to have information"
                    ).set_author(
                        name=str(user)
                    )
                )
                break

            elif entry.target == user:
                # Check if the target is the user that got banned
                await self.log(
                    guild=guild,
                    embed=Embed(
                        color=Color.red()
                    ).set_author(
                        name=str(entry.user)
                    ).add_field(
                        name="banned",
                        value=str(user)
                    ).add_field(
                        name="reason",
                        value=entry.reason
                    )
                )
                break

    async def on_member_unban(self, guild, user):
        # TODO: what if we arent allowed to see audit logs
        # NOTE: we assume the event always gets called before the audit logs get updated
        trigger_time = datetime.datetime.utcnow() - datetime.timedelta(seconds=10)

        # Give Discord some time to put the unban in the audit logs
        await asyncio.sleep(1)

        # Only check unbans and after the time this event got triggered
        async for entry in guild.audit_logs(action=AuditLogAction.unban):
            # NOTE: the `after`-tag in audit_logs seems to get ignored :|, so we have to check manually
            if trigger_time > entry.created_at:
                await self.log(
                    guild=guild,
                    embed=Embed(
                        color=Color.purple(),
                        description="Unban happened, but audit logs dont seem to have information"
                    ).set_author(
                        name=str(user)
                    )
                )
                break

            elif entry.target == user:
                # Check if the target is the user that got unbanned
                await self.log(
                    guild=guild,
                    embed=Embed(
                        color=Color.green()
                    ).set_author(
                        name=str(entry.user)
                    ).add_field(
                        name="unbanned",
                        value=str(user)
                    )
                )
                break

    # ROLES
    async def on_guild_role_create(self, role):
        await self.log(
            guild=role.guild,
            embed=Embed(
                description=role.name,
                color=Color.green()
            ).set_footer(
                text="role created"
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
