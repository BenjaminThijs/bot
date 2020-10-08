import os

all_cogs = os.listdir('cogs')
all_cogs.remove('__init__.py')
all_cogs.remove('cog.py')
all_cogs.remove('__pycache__')

# Remove the .py from each cog
all_cogs = [f"{c[:-3]}" for c in all_cogs]

# Import all the cog files
for c in all_cogs:
    __import__(f"cogs.{c}")

# Get all the cog classes as strings
all_cogs = [f"cogs.{c}.{c.capitalize()}" for c in all_cogs]
