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
brainlets = []
me = '354701063955152898'
eggdra = ['388037798772473859']
sips = ['388839914910908436']
fit = ['423914572148244490']

with open('brainlets.txt') as f:
    brainlets = f.read().splitlines()

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

def write_suggestion(suggestion):
    with open('turtle_quotes.txt', 'a+') as f:
        f.write(suggestion + "\n")

def write_mkid_suggestion(suggestion):
    with open('mkid_quotes.txt', 'a+') as f:
        f.write(suggestion + "\n")

##############
# Bot Events #
##############

# start up confirmation
@bot.event
async def on_ready():
    print("\n-------------------------------")
    print("Quote Bot ready")
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
    
    # get and send message
    message = get_turtle_quote();

    trtl = get(bot.get_all_emojis(), name='trtl')

    await bot.say("{} {} {}".format(str(trtl), message, str(trtl)))

# $insult
@bot.command(pass_context=True)
async def insult(ctx):
    """Outputs a random insult that can be directed through @mentions"""
    command_log.info("%s used $insult" % str(ctx.message.author))
    
    #randomly get message
    message = get_insult()

    # append mentions to message if any mentions
    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            if mention.id == bot.user.id:
                message += str(" <@" + ctx.message.author.id+">")
                await bot.add_reaction(ctx.message, "\u267F")
            
            else:
                message += str(" <@" + mention.id+">")

    await bot.say(message + " \U0001F525")
    #await bot.add_reaction(ctx.message, "\U0001F525")
    return

# $mkidsuggest
@bot.command(pass_context=True)
async def mkidsuggest(ctx):
    suggestion = ctx.message.content[13:]
    command_log.info("%s suggested %s" % (ctx.message.author, suggestion))
    write_mkid_suggestion(suggestion)
    doReset(ctx)

    # give thumbs up reaction
    thumbs_up = get(bot.get_all_emojis(), name='t_ok')
    await bot.add_reaction(ctx.message, thumbs_up)

# $suggest
@bot.command(pass_context=True)
async def suggest(ctx):
    # Can only use $suggest in #fit
    if ctx.message.channel.id not in fit:
        return

    suggestion = ctx.message.content[9:]
    command_log.info("%s suggested %s" % (ctx.message.author, suggestion))
    write_suggestion(suggestion)
    doReset(ctx)
    
    # give thumbs up reaction
    thumbs_up = get(bot.get_all_emojis(), name='t_ok')
    await bot.add_reaction(ctx.message, thumbs_up)

def doReset(ctx):
    """Refreshed data to pull in new quotes and insults"""
    global insults
    global turtle_quotes
    global mkid_quotes
    global thumbs_up
   
    command_log.info("%s used $reset" % str(ctx.message.author))
    
    # reset output arrays
    insults = []
    turtle_quotes = []
    mkid_quotes = []

# $reset
@bot.command(pass_context=True)
async def reset(ctx):
    if ctx.message.author.id in eggdra:
        await bot.say("i don't even care anymore")

    doReset(ctx)

    # give thumbs up reaction
    thumbs_up = get(bot.get_all_emojis(), name='t_ok')
    await bot.add_reaction(ctx.message, thumbs_up)

@bot.command(pass_context=True)
async def addbrainlet(ctx):
    await modifyBrainlet(ctx, remove=False)

async def modifyBrainlet(ctx, remove):
    if ctx.message.author.id != me:
        await bot.add_reaction(ctx.message, get(bot.get_all_emojis(), name='ban'))
        return

    for brainlet in ctx.message.mentions:
        if remove:
            try:
                brainlets.remove(brainlet.id)
            except ValueError:
                pass
        else:
            # don't add to list if already present
            if not brainlet.id in brainlets:
                brainlets.append(brainlet.id)

    with open('brainlets.txt', 'w') as f:
        for b in brainlets:
            f.write(b + "\n")

    await bot.add_reaction(ctx.message, get(bot.get_all_emojis(), name='t_ok'))

@bot.command(pass_context=True)
async def removebrainlet(ctx):
    await modifyBrainlet(ctx, remove=True)

@bot.event
async def on_message(message):
    await addReaction(message, brainlets, ['t_npc'])
    await addReaction(message, eggdra, ['eggdra2'])
    await addReaction(message, sips, ['t_boomer'])
    # process any commands, like $quote
    await bot.process_commands(message)

async def addReaction(message, group, reactions):
    if message.author.id in group:
        for reaction in reactions:
             emote = get(bot.get_all_emojis(), name=reaction)
	     # Don't crash if we can't add a reaction
             try:
                await bot.add_reaction(message, emote)
             except:
                return


#############
# Start Bot #
#############
bot.run(config['token'])
