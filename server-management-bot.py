# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import platform
import datetime
from steem import Steem
from steem.post import Post
from discord.ext.commands import Bot
from discord.ext import commands

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not. Commands are strongly discouraged and will require rewriting a lot of code, edit them into the command() function instead.
client = Bot(description="Server-Management-Bot", command_prefix='!', pm_help = True)
s = Steem()

allowed_channels = ['', # Channels that the bot will monitor, by id.
]

moderating_roles = ['', # Keep them lower case.
]

bot_role = '' # Set a role for all of your bots here. You need to give them such role on the discord server.

channels_list = ['', # Add channels that correspond to the tags bellow.
]

tag_list = ['', # Add your steemit tags for sorting here.
]

#########################
# DEFINE FUNCTIONS HERE #
#########################

async def command(msg,command): # Used to run any commands. Add your commmands here.
	command = str(command)
	command = command[1:]
	if command.startswith('ping'):
		await client.send_message(msg.channel,":ping_pong: Pong!")
	elif command.startswith('users'):
		list_of_users = []
		users_online = client.get_all_members()
		for member in users_online:
			list_of_users.append(member.roles)
		await client.send_message(msg.channel, "There's " + str(len(list_of_users)) + " users online.")
	else:
		command_error = await client.send_message(msg.channel, "Incorrect command.")
		await asyncio.sleep(6)
		await client.delete_message(command_error)

async def del_old_mess(hours): # Deletes posts in channel_list channels older than given hours.
	currtime = datetime.datetime.now() - datetime.timedelta(hours=hours)
	chn = []
	for x in client.get_all_channels():
		if x.id in channels_list:
			chn.append(x)
	for x in chn:
		async for y in client.logs_from(x,limit=100,before=currtime):
			await client.delete_message(y)

async def authorize_post(msg): # Used to authorize posts and sort them into correct channels.
	msg_tag = msg.content.split('/')[3]
	p = Post(msg.content.split('@')[1])
	botmsg = str('This post was nominated by **@' + str(msg.author) + '** and authored by **@' + str(p.author) + '**\n\nTitle: ' + str(p.title) + '\nStatistics: ' + str(p.time_elapsed())[:-10] + ' hours old. Payout: ' + str(p.reward))	

	if check_age(p,2,48):
		feedback_message = await client.send_message(msg.channel, botmsg)
		reaction = await client.wait_for_reaction(['☑'], message=msg, check=is_mod) # Waiting for the emote 
		await client.delete_message(msg)
		await client.delete_message(feedback_message)

		if msg_tag in tag_list: # Sorting the item into a correct channel
			dest_channel = tag_list.index(msg_tag)
		else:
			dest_channel = len(tag_list)

		await client.send_message(client.get_channel(channels_list[dest_channel]), content=msg.content + "\n" + botmsg) # Target channel & message for accepted posts.
	else:
		age_error = await client.send_message(msg.channel, 'Your post has to be between 2h and 48h old.')
		await client.delete_message(msg)
		await asyncio.sleep(6)
		await client.delete_message(age_error)		

def check_age(post,low,high): # Returns true if the post's age is between two dates.
	if post.time_elapsed() > datetime.timedelta(hours=low) and post.time_elapsed() < datetime.timedelta(hours=high):
		return True
	else:
		return False

def is_mod(reaction, user): # Returns true if message's author has a moderating_roles role.
	auth_roles = []
	for x in user.roles:
		auth_roles.append(x.name.lower())

	for x in moderating_roles:
		if x in auth_roles:
			return True
			break
		else:
			return False

######################
# DEFINE EVENTS HERE #
######################

@client.event
async def on_ready():
	print('\nUse this link to invite {}:'.format(client.user.name))
	print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('BasicBot created by Habchy#1665')
	print('--------')
	print('Code altered to work with STEEM by Vctr#5566')
	print('--------')
	print('Steemit profile: https://steemit.com/@jestemkioskiem')


# This is our event check. For simplicity's sake, everything happens here. You may add your own events, but commands are discouraged, for that, edit the command() function instead.
@client.event
async def on_message(message):
	await del_old_mess(132)

	if message.content.startswith(client.command_prefix): # Setting up commands. You can add new commands in the commands() function at the top of the code.
		await command(message, message.content)

	elif bot_role not in [y.name.lower() for y in message.author.roles] and message.channel.id in allowed_channels: # Checking if the poster wasn't the bot and if it was in one of the monitored channels.
		if message.content.startswith('https://steemit.com') or message.content.startswith('https://busy.org'): # The required beggining of a text for it to be considered not spam.	
			await authorize_post(message)
		else:
			if not is_mod(reaction=None, user=message.author):
				await client.delete_message(message)
				link_error = await client.send_message(message.channel, content= '@' + str(message.author) + ' Your link has to start with "https://steemit.com" or "https://busy.org"')
				await asyncio.sleep(6)
				await client.delete_message(link_error)	

client.run('') # <----------- PUT YOUR BOT'S TOKEN HERE!

# Basic Bot was created by Habchy#1665
# Thank you for using this and don't forget to star Habchy's repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# STEEM's functionality was coded by Vctr#5566, or @jestemkioskiem on steem and steem chat. Contact him if you have any questions.