from discord.ext import commands
import cogs

# Just making sure the token is in a private file that will never be pushed
def retrieve_token():
    with open("token", "r") as token_file:
        return token_file.read()

# Create the bot instance
bot = commands.Bot(command_prefix="$", case_insensitive=True)

# Initialize all cogs and load them
for c in cogs.all_cogs:
    bot.add_cog(eval(c)(bot))

# This is just so the bot owner knows the bot is online
# It serves no functional purpose
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

# We want to make sure we can turn the bot off
# TODO: remove this once in production, or make sure only the bot owner can do this.
@bot.command(name="stop", aliases=["exit", "off"], brief="Turn off the bot")
async def stop(ctx):
    await ctx.send("Bye bye")
    await bot.close()


# Run the botloop, in case we stop the bot by force we have a try except around it.
try:
    bot.run(retrieve_token())
except KeyboardInterrupt:
    bot.close()
