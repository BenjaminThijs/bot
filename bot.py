from discord.ext import commands
import cogs

def retrieve_token():
    with open("token", "r") as token_file:
        return token_file.read()

bot = commands.Bot(command_prefix="$", case_insensitive=True)

# Initialize all cogs and load them
for c in cogs.all_cogs:
    bot.add_cog(eval(c)())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(name="stop", aliases=["exit", "off"])
async def stop(ctx, *args):
    await ctx.send("Bye bye")
    await bot.close()


try:
    bot.run(retrieve_token())
except:
    bot.close()
