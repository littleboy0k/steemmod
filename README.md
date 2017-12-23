# steemit-moderation
Repository of open source tools used by steemit moderation community.
The repository currently includes:
* *Marshal* the server manager
* *stbot* the payout calculator

## Requirements:
#### Python:
* Written in Python 3.6.3
* Requires at least Python3
#### Directories:
* steem API ([steem-python](https://github.com/steemit/steem-python))
* discord API ([discord.py](https://github.com/Rapptz/discord.py))

## Running:
```PAYOUT_BOT_TOKEN=BOT_TOKEN python3.6 stbot.py``` to run stbot

```MANAGEMENT_BOT_TOKEN=BOT_TOKEN python3.6 server-management-bot.py``` to run Marshal

# Marshal
Marshal, the server-management-bot was built for the steemit moderation project by [Jestemkioskiem](https://github.com/Jestemkioskiem) (https://steemit.com/@jestemkioskiem/)

## Functionality:

* Easily editable - a good base for any steem discord related bot.
* Easily add custom commands by editing the command() function;
* Submit a post by posting a message starting with *https://steemit.com* or *https://busy.org* in an allowed channel;
* Accept a post by reacting to it - by default use :ballot_box_with_check: on a given post;
* Sort accepted posts into correct channels by the tag they were posted under;
* Remove accepted posts older than x hours;

# stbot
**stbot** was built for the steemit moderation project by [Emre](https://github.com/emre) (https://steemit.com/@emrebeyler).

## Functionality:

#### Check various stats about a steem post and check how much of the payout was given by bots.
* **Total Payout** - Total value of the payout for a given post in $ (Neither USD nor SBD, but rather the $ steem shows under the post).
* **Organic** - The ammount given by non-bot users.
* **Bots** - The ammount given by bot users.
* **Net Votes** - Total ammount of votes, regardles of who the user is.
* **Comments** - Number of comments under the post.
* **Age** - The age of the post. 

