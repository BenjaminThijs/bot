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

# This code runs once the bot is connected to Discord
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Get the admin_cog
    admin_cog = bot.get_cog("Admin")

    # The bot has just started up, we need to check if we need to start the monitor_loop
    if len(admin_cog.settings["monitor"]) > 0:
        print(f"Starting monitoring loop")
        admin_cog.monitor_loop.start()

# We want to make sure we can turn the bot off
# TODO: remove this once in production, or make sure only the bot owner can do this.
@bot.command(name="stop", aliases=["exit", "off"], brief="Turn off the bot")
async def stop(ctx):
    await ctx.send("Bye bye")
    await bot.close()

# Reload command, reloads all the cogs
@bot.command(name="reload", brief="Reload all cogs")
async def reload(ctx):
    for c in list(bot.cogs):
        bot.remove_cog(c)

    for c in cogs.all_cogs:
        bot.add_cog(eval(c)(bot))

    await ctx.send("Done reloading")

# Run the botloop, in case we stop the bot by force we have a try except around it.
try:
    bot.run(retrieve_token())
except KeyboardInterrupt:
    bot.close()
