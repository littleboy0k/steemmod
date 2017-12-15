import logging
import os

from steem import Steem
from steem.amount import Amount
from steem.post import Post
from discord.ext.commands import Bot

logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)
logging.basicConfig()


client = Bot(description="Post Bot",
             command_prefix="$", pm_help=False)

BOT_LIST = [
    'animus',
    'appreciator',
    'arama',
    'ausbitbot',
    'bago',
    'bambam808',
    'banjo',
    'barrie',
    'bellyrub',
    'besttocome215',
    'bierkaart',
    'biskopakon',
    'blackwidow7',
    'blimbossem',
    'boomerang',
    'booster',
    'boostupvote',
    'bowlofbitcoin',
    'bp423',
    'brandybb',
    'brensker',
    'btcvenom',
    'buildawhale',
    'burdok213',
    'businessbot',
    'centerlink',
    'cleverbot',
    'cnbuddy',
    'counterbot',
    'crypto-hangouts',
    'cryptobooty',
    'cryptoholic',
    'cryptoowl',
    'cub1',
    'curationrus',
    'dahrma',
    'davidding',
    'decibel',
    'deutschbot',
    'dirty.hera',
    'discordia',
    'done',
    'drakkald',
    'drotto',
    'earthboundgiygas',
    'edrivegom',
    'emilhoch',
    'eoscrusher',
    'famunger',
    'feedyourminnows',
    'followforupvotes',
    'frontrunner',
    'fuzzyvest',
    'gamerpool',
    'gamerveda',
    'gaming-hangouts',
    'gindor',
    'givemedatsteem',
    'givemesteem1',
    'glitterbooster',
    'gonewhaling',
    'gotvotes',
    'gpgiveaways',
    'gsgaming',
    'guarddog',
    'heelpopulair',
    'helpfulcrypto',
    'idioticbot',
    'ikwindje',
    'ilvacca',
    'inchonbitcoin',
    'ipuffyou',
    'lovejuice',
    'mahabrahma',
    'make-a-whale',
    'makindatsteem',
    'maradaratar',
    'minnowbooster',
    'minnowhelper',
    'minnowpond',
    'minnowpondblue',
    'minnowpondred',
    'misterwister',
    'moonbot',
    'morwhale',
    'moses153',
    'moyeses',
    'msp-lovebot',
    'msp-shanehug',
    'msp-venezuela',
    'msp-music',
    'msp-mods',
    'msp-africa',
    'msp-canada',
    'muxxybot',
    'myday',
    'ninja-whale',
    'ninjawhale',
    'officialfuzzy',
    'perennial',
    'pimpoesala',
    'polsza',
    'portoriko',
    'prambarbara',
    'proctologic',
    'pumpingbitcoin',
    'pushup',
    'qurator',
    'qwasert',
    'raidrunner',
    'ramta',
    'randovote',
    'randowhale',
    'randowhale0',
    'randowhale1',
    'randowhaletrail',
    'randowhaling',
    'reblogger',
    'resteem.bot',
    'resteemable',
    'resteembot',
    'russiann',
    'scamnotifier',
    'scharmebran',
    'siliwilly',
    'sneaky-ninja',
    'sniffo35',
    'soonmusic',
    'spinbot',
    'stackin',
    'steemedia',
    'steemholder',
    'steemit-gamble',
    'steemit-hangouts',
    'steemitgottalent',
    'steemmaker',
    'steemmemes',
    'steemminers',
    'steemode',
    'steemprentice',
    'steemsquad',
    'steemthat',
    'steemvoter',
    'stephen.king989',
    'tabea',
    'tarmaland',
    'timbalabuch',
    'trail1',
    'trail2',
    'trail3',
    'trail4',
    'trail5',
    'trail6',
    'trail7',
    'viraltrend',
    'votey',
    'waardanook',
    'wahyurahadiann',
    'wannabeme',
    'weareone1',
    'whatamidoing',
    'whatupgg',
    'wildoekwind',
    'wiseguyhuh',
    'wistoepon',
    'zdashmash',
    'zdemonz',
    'jamesbarraclough',
    'rocky1',
    'pula78',
    'tayyabhussain',
    'malikidrees',
    'sanamamq',
    'mamqmuqit',
    'kalinka',
    'lays',
    'aksdwi',
    'jamessmith0',
    'hamza-arshad',
    'aqibwarsi',
    'akshaykumar12257',
    'withsmn',
    'aafrin',
    'zhusatriani'
]
MINIMUM_RSHARE_PAYOUT = +0.1
POST_PAYOUT_BOT_CHANNEL_NAME = "statistics"

s = Steem()


def elapsed_time_in_str(delta):

    if delta.days > 0:
        return "%s days" % delta.days
    if delta.seconds / 3600 > 0:
        return "%s hours" % (int(delta.seconds / 3600))
    if delta.minutes / 60 > 0:
        return "%s minutes" % (int(delta.minutes / 60))

    return ""


def get_payout_from_rshares(rshares, reward_balance,
                            recent_claims, base_price):
    fund_per_share = Amount(reward_balance).amount / float(recent_claims)
    payout = float(rshares) * fund_per_share * Amount(base_price).amount

    return payout


def get_post_details(s, identifier):
    try:
        p = Post(identifier)
    except Exception as error:
        return {
            "error": "Couldn't fetch the post.",
            "message": str(error),
        }

    reward_fund = s.get_reward_fund()
    reward_balance, recent_claims = reward_fund["reward_balance"], \
                                    reward_fund["recent_claims"]
    base_price = s.get_current_median_history_price()["base"]

    total_payout = 0
    bot_payout = 0
    used_bots = []
    for vote in p.get("active_votes", []):
        vote_payout = get_payout_from_rshares(
            vote["rshares"], reward_balance, recent_claims, base_price)

        if vote["voter"] in BOT_LIST and vote_payout > MINIMUM_RSHARE_PAYOUT:
            bot_payout += vote_payout
            used_bots.append({
                "bot": vote["voter"],
                "payout": round(vote_payout, 2),
            })

        total_payout += vote_payout

    stats = {
        "total": round(total_payout, 2),
        "bot": round(bot_payout, 2),
        "organic": round((total_payout - bot_payout), 2),
        "net_votes": p["net_votes"],
        "elapsed_time": p.time_elapsed(),
        "comment_count": p.children,
    }

    return stats


@client.event
async def on_ready():
    logger.info("Logged in.")


@client.event
async def on_message(message):
    if message.channel.name != POST_PAYOUT_BOT_CHANNEL_NAME:
        logger.info("Incorrect channel")
        return

    if '@' not in message.content:
        logger.info("incorrect url")
        return

    stats = get_post_details(s, message.content)
    if 'error' in stats:
        await client.say("Error: %s" % stats["message"])

    reply = "Total Payout: **$%s**. (Organic: **$%s**, Bots: **$%s**) "
    reply += "Net Votes: **%s**. Comments: **%s**. (*%s old.*)"

    reply = reply % (
        stats["total"],
        stats["organic"],
        stats["bot"],
        stats["net_votes"],
        stats["comment_count"],
        elapsed_time_in_str(stats["elapsed_time"])
    )

    await client.send_message(message.channel, content=reply)


if __name__ == '__main__':
    client.run(os.getenv('PAYOUT_BOT_TOKEN'))


