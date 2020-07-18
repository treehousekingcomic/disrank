# Disrank (THKC FORKED)
A lib to make good looking discord profile card.
Forked to use "`class object`" mode like discord.Embed
First you initiate disrank with the`DisrankGenerator`, then to get your disrank just do DisrankObject.generate()

# Usage
```py
from disrank import DisrankGenerator

args = {
	'bg_image' : '', # Background image link 
	'profile_image' : '', # User profile picture link
	'level' : 1, # User current level 
	'current_xp' : 0, # Current level minimum xp 
	'user_xp' : 10, # User current xp
	'next_xp' : 100, # xp required for next level
	'user_position' : 1, # User position in leaderboard
	'user_name' : 'Name#0001', # user name with descriminator 
	'user_status' : 'online', # User status eg. online, offline, idle, streaming, dnd
}


card = DisrankGenerator(**args)
image = card.generate()

# In a discord command
file = discord.File(fp=image, filename='image.png')
await ctx.send(file=file)
```

Make sure to run the generate part in an executor. 
[Join here](https://discord.gg/7SaE8v2) for help. 
**NOTE:** The server above is the original server of disrank, you might not get helped with this easier foked repository.
