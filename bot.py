import asyncio
import discord
from discord.ext import commands
import json
import random

config = json.load(open('config.json'))
insults = []
mkid_quotes = []

bot = commands.Bot(
                command_prefix='$',
                description='insult bot',
                pm_help=False)


def get_insult():
    global insults
    if not insults:
        with open('insults.txt') as f:
            insults = f.read().splitlines()
    r = random.randint(0,len(insults)-1)
    return insults[r]


def get_mkid_quote():
    global mkid_quotes
    if not mkid_quotes:
        with open('mkid_quotes.txt') as f:
            mkid_quotes = f.read().splitlines()
    r = random.randint(0, len(mkid_quotes)-1)
    return mkid_quotes[r]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def mkid(ctx):
    member = ctx.message.server.get_member(str(bot.user.id))
    await bot.change_nickname(member, "Mkid Quotes")
    message = get_mkid_quote();
    await bot.say("\"%s\" - mkid" % message)
 


@bot.command(pass_context=True)
async def insult(ctx):
    member = ctx.message.server.get_member(str(bot.user.id))
    await bot.change_nickname(member, "Burn Bot")
 
    #randomly get message
    message = get_insult()


    if ctx.message.mentions:
        for mention in ctx.message.mentions:
            if mention.id == "409953598194057218" or mention.id == bot.user.id:
                message += str(" <@" + ctx.message.author.id+">")
                await bot.add_reaction(ctx.message, "\u267F")
            
            else:
                message += str(" <@" + mention.id+">")



    await bot.say(message + " \U0001F525")
    #await bot.add_reaction(ctx.message, "\U0001F525")
    return


bot.run(config['token'])
