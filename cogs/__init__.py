import os

# Get all the cog files
# TODO: this assumes all files in cogs/ are cog files, should this change?
all_cogs = os.listdir('cogs')

# Some of the files (and a folder) are not cogs
all_cogs.remove('__init__.py')
all_cogs.remove('cog.py')
all_cogs.remove('__pycache__')

# Remove the .py from each cog filename
all_cogs = [f"{c[:-3]}" for c in all_cogs]

# Import all the cogs using their filename
for c in all_cogs:
    __import__(f"cogs.{c}")

# Get all the cog classes as strings
# TODO: this assumes the cog-classname is the same as the filename using capitalization
# TODO: should this change? Or simply be properly documented?
all_cogs = [f"cogs.{c}.{c.capitalize()}" for c in all_cogs]
