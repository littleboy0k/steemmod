	# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import datetime
from steem import Steem
from steem.post import Post
from discord.ext.commands import Bot
from discord.ext import commands

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not. @client.command is strongly discouraged, edit your commands into the command() function instead.
client = Bot(description="Server-Management-Bot", command_prefix='!', pm_help = True)
s = Steem()

bot_role = 'marshal' # Set a role for all of your bots here. You need to give them such role on the discord server.

allowed_channels = ['387030201961545728', #community-review
]

moderating_roles = ['developers', # Keep them lower case.
'moderators']

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
'389764366456586240' #all_other
]

tag_list = ['introduceyourself',
'steemit',
'bitcoin',
'cryptocurrency',
'blog',
'steem',
'crypto',
'health',
'science',
'technology',
'programming',
'tutorials']

#########################
# DEFINE FUNCTIONS HERE #
#########################

 # Used to run any commands. Add your custom commands here, each under a new elif command.startswith(name):.
async def command(msg,command):
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

	elif command.startswith('hey'):
		await client.send_message(msg.channel, "Hey, utopian!")
	
	else:
		command_error = await client.send_message(msg.channel, "Incorrect command.")
		await asyncio.sleep(6)
		await client.delete_message(command_error)

# Deletes posts in channel_list channels older than given hours.
async def del_old_mess(hours): 
	currtime = datetime.datetime.now() - datetime.timedelta(hours=hours)
	chn = []
	for x in client.get_all_channels():
		if x.id in channels_list:
			chn.append(x)
	for x in chn:
		async for y in client.logs_from(x,limit=100,before=currtime):
			await client.delete_message(y)

# Used to authorize posts and sort them into correct channels.
async def authorize_post(msg): 
	msg_tag = msg.content.split('/')[3]
	p = Post(msg.content.split('@')[1])
	botmsg = str('Title: ' + str(p.title) + '\n\nThis post was nominated by **@' + str(msg.author) + '** and authored by **@' + str(p.author) + '**\nStatistics: ' + str(p.time_elapsed())[:-10] + ' hours old. Payout: ' + str(p.reward))	

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

# Returns true if the post's age is between two dates.
def check_age(post,low,high): 
	if post.time_elapsed() > datetime.timedelta(hours=low) and post.time_elapsed() < datetime.timedelta(hours=high):
		return True
	else:
		return False

# Returns true if message's author has a moderating_roles role.
def is_mod(reaction, user): 
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
	print('\nInvite link: https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
	print('--------')
	print('Server-Management-Bot was built by Vctr#5566')
	print('Steemit profile: https://steemit.com/@jestemkioskiem')


# This is our event check. For simplicity's sake, everything happens here. You may add your own events, but commands are discouraged, for that, edit the command() function instead.
@client.event
async def on_message(message):
	
	await del_old_mess(132)

	if message.content.startswith(client.command_prefix): # Setting up commands. You can add new commands in the commands() function at the top of the code.
		await command(message, message.content)

	elif bot_role not in [y.name.lower() for y in message.author.roles] and message.channel.id in allowed_channels: # Checking if the poster wasn't the bot and if it was in one of the monitored channels.
		if message.content.startswith('https://steemit.com') or message.content.startswith('https://busy.org'):
			await authorize_post(message)
		else:
			if not is_mod(reaction=None, user=message.author):
				await client.delete_message(message)
				link_error = await client.send_message(message.channel, content= '@' + str(message.author) + ' Your link has to start with "https://steemit.com" or "https://busy.org"')
				await asyncio.sleep(6)
				await client.delete_message(link_error)	

if __name__ == '__main__': # Starting the bot.
	client.run(os.getenv('MANAGEMENT_BOT_TOKEN')

# This was initially built upon BasicBot, although the original code is long gone. Still, I'll give the credit where credit is due. [Repo Link: https://github.com/Habchy/BasicBot]

# This was coded by Vctr#5566, or @jestemkioskiem on steem steem chat and github. Contact him if you have any questions.
