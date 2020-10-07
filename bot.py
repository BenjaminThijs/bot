from discord.ext import commands
from admin import Admin

def retrieve_token():
    with open("token", "r") as token_file:
        return token_file.read()

bot = commands.Bot(command_prefix="$", case_insensitive=True)
bot.add_cog(Admin())

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
