# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Placeholder", command_prefix="!", pm_help = True)

# Add your channels there, by ID. This will be necessary for moving around the server.

channels_list = ['389762510779187200', #introduceyourself
'389608804972756993', #steemit
'389762038408282112', #bitcoin
'389762302330535946', #cryptocurrency
'389762891823316992', #blog
'389761959014432778', #steem
'389764215537270787', #crypto
'389764282700660737', #health
'389764314313129984', #science
'389890366427627520', #technology
'389890644551794688', #programming
'389890578499764226', #tutorials
'389764366456586240' #all-other
]

allowed_channels = ['387030201961545728', #community-review

]

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.
@client.event
async def on_ready():
	print('Logged in as '+client.user.name+' (ID:'+client.user.id+') | Connected to '+str(len(client.servers))+' servers | Connected to '+str(len(set(client.get_all_members())))+' users')
	print('--------')
	print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__, platform.python_version()))
	print('--------')
	print('Use this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Github Link: https://github.com/Habchy/BasicBot')
	print('--------')
	print('BasicBot created by Habchy#1665')
	print('--------')
	print('Code altered to work with STEEM by Vctr#5566')
	print('--------')
	print('Steemit profile: https://steemit.com/@jestemkioskiem')

# This is a basic example of a call and response command. You tell it do "this" and it does it.

@client.event
async def on_message(message):
	msg = message
	msgcon = msg.content
	msgaut = '@' + msg.author.name

	if "steemit-moderator" not in [y.name.lower() for y in message.author.roles] and message.channel.id in allowed_channels:
		if message.content.startswith('https://steemit') or message.content.startswith('steemit'): # The required beggining of a text for it to be considered not spam.			
			tempmsg = await client.send_message(message.channel, 'Your submition awaits for Moderator\'s feedback') # Return message after a correct submition.
			
			res = await client.wait_for_reaction(['☑'], message=msg)
			if "developers" in [y.name.lower() for y in res.user.roles] or "moderators" in [y.name.lower() for y in res.user.roles]: # Name of the role meant to accept posts.
				await client.delete_message(msg)
				await client.delete_message(tempmsg)
				await client.send_message(client.get_channel(channels_list[12]), content=msgaut + ' sent: ' + msgcon) # Target channel for accepted posts, check the number of desired channel in the list on top of the code.
		
		elif message.content.startswith('!ping') and "developers" in [y.name.lower() for y in message.author.roles] or "moderators" in [y.name.lower() for y in message.author.roles]:
			await client.send_message(message.channel, ':ping_pong: Pong! I\'m live and working correctly!')

		else:
			await client.delete_message(msg)
			await client.send_message(message.channel, content=msgaut + ' Your link has to start with "https://steemit" or "steemit"') # Return text for a incorrect sumbition.
	
client.run('MzkxMDczNjgzNTk2MjQ3MDQw.DRTbpQ.0kipdJjxdKSlERdeKkzSt11tut8')

# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False" on line 9.