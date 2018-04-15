# Created By: Wesley
# Date: 4/2/18

import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import json
import random
import logging
import datetime

###########
# Logging #
###########
logging.basicConfig(filename='basic.log',level=logging.WARNING)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

# setup manual logging
command_log = logging.getLogger("manual")
command_log.setLevel(logging.INFO)
command_log.addHandler(logging.FileHandler("discord_commands.log", encoding='utf-8', mode='a+'))

# setup logger with python discord api
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='a+')
handler.setFormatter(formatter)
logger.addHandler(handler)


#################
# Initial Setup #
#################

# init config
config = json.load(open('config.json'))

# output arrays
insults = []
turtle_quotes = []
mkid_quotes = []

# turtle traders id
turtle_traders = "413834195220037640"

# config bot defaults
bot = commands.Bot(
                command_prefix='$',
                description='insult bot',
                pm_help=False)


####################
# Helper Functions #
####################

# returns random line from insults.txt
def get_insult():
    global insults
    if not insults:
        with open('insults.txt') as f:
            insults = f.read().splitlines()
    r = random.randint(0,len(insults)-1)
    return insults[r]

# returns a random mkid quote
def get_mkid_quote():
    global mkid_quotes
    if not mkid_quotes:
        with open('mkid_quotes.txt') as f:
            mkid_quotes = f.read().splitlines()
    r = random.randint(0, len(mkid_quotes)-1)
    return mkid_quotes[r]

# returns a random turtle quote
def get_turtle_quote():

    global turtle_quotes

    # read from file if empty
    if not turtle_quotes:
        with open('turtle_quotes.txt') as f:
            turtle_quotes = f.read().splitlines()
           
    r = random.randint(0, len(turtle_quotes)-1)
    return turtle_quotes[r]

# write user suggestion to the sugguestion.txt file to be manually added if acceptable
def write_suggestion(suggestion):
    with open('suggestions.txt', 'a+') as f:
        f.write(suggestion + "\n")


##############
# Bot Events #
##############

# start up confirmation
@bot.event
async def on_ready():
    print("\n-------------------------------")
    print("Burn Bot ready")
    print('Logged in as %s' % bot.user.name)
    print("-------------------------------\n")
    logger.info("Bot Started")


###############
# Bot Commands #
###############

# $mkid
@bot.command(pass_context=True)
async def mkid(ctx):
    """Outputs a random mkid quote"""    
    command_log.info("%s used $mkid" % str(ctx.message.author))
    
    # get and send message
    message = get_mkid_quote();
    await bot.say(message + " :dog:")

# $quote
@bot.command(pass_context=True)
async def quote(ctx):
    """Outputs a random turtle quote"""
    
    command_log.info("%s used $quote" % str(ctx.message.author))
    
    # only function in turtle traders
    global turtle_traders
    print(ctx.message.server)
    if turtle_traders not in ctx.message.server:
        return
    
    # get and send message
    message = get_turtle_quote();
    await bot.say("<:trtl:413861615973433383> " + message + " <:trtl:413861615973433383>")

# $insult
@bot.command(pass_context=True)
async def insult(ctx):
    """Outputs a random insult that can be directed through @mentions"""
    command_log.info("%s used $insult" % str(ctx.message.author))
    
    # only function in turtle traders
    global turtle_traders
    if turtle_traders != ctx.message.server:
        return


    #randomly get message
    message = get_insult()

    # append mentions to message if any mentions
    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            # refuse insult mentions at wesley or bot
            if mention.id == "409953598194057218" or mention.id == bot.user.id:
                message += str(" <@" + ctx.message.author.id+">")
                await bot.add_reaction(ctx.message, "\u267F")
            
            else:
                message += str(" <@" + mention.id+">")

    await bot.say(message + " \U0001F525")
    #await bot.add_reaction(ctx.message, "\U0001F525")
    return

# $suggest
@bot.command(pass_context=True)
async def suggest(ctx):
    """Can be used to suggest new quotes or insults to be added to the bot after being reiewed"""
    suggestion = ctx.message.content[9:]
    command_log.info("%s suggested %s" % (ctx.message.author, suggestion))
    write_suggestion(suggestion)
    
    # give thumbs up reaction
    thumbs_up = get(bot.get_all_emojis(), name='t_ok')
    await bot.add_reaction(ctx.message, thumbs_up)

# $reset
@bot.command(pass_context=True)
async def reset(ctx):
    """Refreshed data to pull in new quotes and insults"""
    global insults
    global turtle_quotes
    global mkid_quotes
    global thumbs_up
   
    command_log.info("%s used $reset" % str(ctx.message.author))
    
    # reset name to Burn Bot
    member = ctx.message.server.get_member(str(bot.user.id))
    await bot.change_nickname(member, "Burn Bot")
    
    # reset output arrays
    insults = []
    turtle_quotes = []
    mkid_quotes = []

    # give thumbs up reaction
    thumbs_up = get(bot.get_all_emojis(), name='t_ok')
    await bot.add_reaction(ctx.message, thumbs_up)


#############
# Start Bot #
#############
bot.run(config['token'])

