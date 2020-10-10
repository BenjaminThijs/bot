import bot
import cogs

# Just making sure the token is in a private file that will never be pushed
def retrieve_token():
    with open("token", "r") as token_file:
        return token_file.read()

# Create the bot instance
bot = bot.Bot(command_prefix="$", case_insensitive=True)

# Run the botloop, in case we stop the bot by force we have a try except around it.
try:
    bot.run(retrieve_token())
except KeyboardInterrupt:
    bot.close()
