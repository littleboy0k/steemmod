	# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
import datetime
from steem import Steem
from steem.post import Post
from steem.instance import set_shared_steemd_instance
from steem.steemd import Steemd
from discord.ext.commands import Bot
from discord.ext import commands
from coinmarketcap import Market
import os

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not. @client.command is strongly discouraged, edit your commands into the command() function instead.
client = Bot(description="Server-Management-Bot", command_prefix='!', pm_help = True)

s = Steem()
steemd_nodes = [
    'https://api.steemit.com/',
    'https://gtg.steem.house:8090/',
    'https://steemd.steemitstage.com/',
    'https://steemd.steemgigs.org/'
    'https://steemd.steemit.com/',
]
set_shared_steemd_instance(Steemd(nodes=steemd_nodes)) # set backup API nodes

cmc = Market() # Coinmarketcap API call.
ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")

react_dict = {}

bot_role = 'bots' # Set a role for all of your bots here. You need to give them such role on the discord server.

allowed_channels = ['402402513321721857', #review-linkdrop
'399691348028030989' # testing:
]

moderating_roles = ['developers', # Keep them lower case.
'moderators']

# channels
channels = [
	{
		'name': 'introduceyourself',
		'id_community': '393994169955385355',
		'id_verified': '389762510779187200'
	},
	{
		'name': 'steemit',
		'id_community': '393999443877429248',
		'id_verified': '389608804972756993'
	},
	{
		'name': 'bitcoin',
		'id_community': '393999470427242497',
		'id_verified': '389762038408282112'
	},
	{
		'name': 'cryptocurrency',
		'id_community': '393999513012011009',
		'id_verified': '389762302330535946'
	},
	{
		'name': 'blog',
		'id_community': '393999532066865153',
		'id_verified': '389762891823316992'
	},
	{
		'name': 'steem',
		'id_community': '393999563415093257',
		'id_verified': '389761959014432778'
	},
	{
		'name': 'crypto',
		'id_community': '393999585397440522',
		'id_verified': '389764215537270787'
	},
	{
		'name': 'health',
		'id_community': '393999638174367746',
		'id_verified': '389764282700660737'
	},
	{
		'name': 'science',
		'id_community': '393999658411622401',
		'id_verified': '389764314313129984'
	},
	{
		'name': 'technology',
		'id_community': '393999682889842688',
		'id_verified': '389890366427627520'
	},
	{
		'name': 'programming',
		'id_community': '393999709796171777',
		'id_verified': '389890644551794688'
	},
	{
		'name': 'tutorials',
		'id_community': '393999737864454144',
		'id_verified': '389890578499764226'
	},
	{
		'name': 'all_other',
		'id_community': '393999762820694017',
		'id_verified': '389764366456586240'
	},
	# # testing:
	# {
		# 'name': 'tematygodnia',
		# 'id_community': '403670427442085888',
		# 'id_verified': '403284221713711105'
	# }
]

link_only_channels = [ # Put all the channels that are exclusively for sharing links into this list.
'402402513321721857' # review_linkdrop
]


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

# Deletes posts in channels older than given hours.
async def del_old_mess(hours): 
	currtime = datetime.datetime.now() - datetime.timedelta(hours=hours)
	chn = []
	for x in client.get_all_channels():
		if x.id in [channel['id_community'] for channel in channels]: #channels_list:
			chn.append(x)
	for x in chn:
		async for y in client.logs_from(x,limit=100,before=currtime):
			await client.delete_message(y)

async def payout(total,sbd,ste):
	total = float(total) * 0.8 # Currator cut, anywhere between 0.85 and 0.75.
	totalsbd = str(total * 0.5 * float(sbd))[:6]
	totalsp = total * 0.5 * float(ste)
	totalsp = str(totalsp * 1/float(ste))[:6] # SBD is always worth 1$ in the steem blockchain, so price of SBD to price of STE is always 1/STE.
	payout = str(float(totalsbd) + float(totalsp))[:6]
	return payout

async def get_info(msg):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])
	embed=discord.Embed(color=0xe3b13c)
	embed.add_field(name="Title", value=str(p.title), inline=False)
	embed.add_field(name="Author", value=str("@"+p.author), inline=True)
	embed.add_field(name="Nominator", value=str('<@'+ msg.author.id +'>'), inline=True)
	embed.add_field(name="Age", value=str(p.time_elapsed())[:-10] +" hours", inline=False)
	embed.add_field(name="Payout", value=str(p.reward), inline=True)
	embed.add_field(name="Payout in USD", value=await payout(p.reward,sbd_usd,ste_usd), inline=True)
	return embed


# Used to sort post into correct channels.
async def sort_post(msg):
	dest_channel = None
	msg_tag = msg.content.split('/')[3]
	p = Post(msg.content.split('@')[1])

	for channel in channels:
		if channel['name'] == msg_tag:
			dest_channel = channel['id_community']
			break
	if dest_channel == None:
		dest_channel = channels[len(channels)-1]['id_community'] # others as default
		
	embed = await get_info(msg)
	if embed:
		new_msg = await client.send_message(client.get_channel(dest_channel), content=msg.content) # send original message
		embed_msg = await client.send_message(client.get_channel(dest_channel), embed=embed) # send embed
		comment_msg = await client.send_message(client.get_channel(dest_channel), content="This post was submitted in the server by <@" + msg.author.id + ">" ) # send comment

		react_dict[new_msg.id] = [new_msg.id, embed_msg.id, comment_msg.id] # store new messages ids
		await client.delete_message(msg) # delete old message
		
		if dest_channel:
			response = await client.send_message(msg.channel, "Post was moved to channel <#" + dest_channel + ">")
			await asyncio.sleep(6)
			await client.delete_message(response)


# Used to authorize posts and sort them into correct channels.
async def authorize_post(msg, user): 
	dest_channel = None
	msg_tag = msg.content.split('/')[3]
	p = Post(msg.content.split('@')[1])
	
	for channel in channels:
		if channel['name'] == msg_tag:
			dest_channel = channel['id_verified']
			break
	if dest_channel == None:
		dest_channel = channels[len(channels)-1]['id_verified'] # others as default

	embed = await get_info(msg)
	if embed:
		await client.send_message(client.get_channel(dest_channel), content=msg.content) # send original message
		await client.send_message(client.get_channel(dest_channel), embed=embed) # send embed
		await client.send_message(client.get_channel(dest_channel), content="This post was accepted by <@" + user.id + ">" ) # send comment
		
		# delete old messages
		for msg_id in react_dict[msg.id]:
			msg = await client.get_message(msg.channel, msg_id)
			await client.delete_message(msg)
		
		if dest_channel:
			response = await client.send_message(msg.channel, "Post was moved to channel <#" + dest_channel + ">")
			await asyncio.sleep(6)
			await client.delete_message(response)
			
async def is_link(msg):
	if bot_role not in [y.name.lower() for y in msg.author.roles] and msg.channel.id in link_only_channels:
		if msg.content.startswith("https://steemit.com"):
			return True
		else:
			await client.delete_message(msg)
			response = await client.send_message(msg.channel, "Only links starting with https://steemit.com are allowed in this channel.")
			await asyncio.sleep(6)
			await client.delete_message(response)


async def check_reward(msg):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])
	
	reward = float(str(p.reward).replace(" SBD", ""))

	if reward > 30:
		await client.delete_message(msg)
		response = await client.send_message(msg.channel, "Your post already has a high payout. Only posts with lower than 30 SBD payout are allowed.")
		await asyncio.sleep(6)
		await client.delete_message(response)
		return False
	else:
		return True	


# Returns true if the post's age is between two dates.
async def check_age(msg,low,high):
	link = str(msg.content).split(' ')[0]
	p = Post(link.split('@')[1])

	if p.time_elapsed() > datetime.timedelta(hours=low) and p.time_elapsed() < datetime.timedelta(hours=high):
		return True
	else:
		age_error = await client.send_message(msg.channel, 'Your post has to be between 2h and 48h old.')
		await client.delete_message(msg)
		await asyncio.sleep(6)
		await client.delete_message(age_error)
		return False

# Returns true if message's author has a moderating_roles role.
def is_mod(user): 
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
	ste_usd = cmc.ticker("steem", limit="3", convert="USD")[0].get("price_usd", "none")
	sbd_usd = cmc.ticker("steem-dollars", limit="3", convert="USD")[0].get("price_usd", "none")
	await del_old_mess(132)

	if await is_link(message):
		if await check_age(message, 2, 48):
			await check_reward(message)

	if message.content.startswith(client.command_prefix): # Setting up commands. You can add new commands in the commands() function at the top of the code.
		await command(message, message.content)

	elif bot_role not in [y.name.lower() for y in message.author.roles] and message.channel.id in allowed_channels: # Checking if the poster wasn't the bot and if it was in one of the monitored channels.
		if message.content.startswith('https://steemit.com'):
			await sort_post(message)

@client.event
async def on_reaction_add(reaction, user):
	if is_mod(user):
		if reaction.emoji == '☑' and reaction.message.channel.id in [channel['id_community'] for channel in channels]:
			await authorize_post(reaction.message, user)

if __name__ == '__main__': # Starting the bot.
	client.run(os.getenv('TOKEN'))
