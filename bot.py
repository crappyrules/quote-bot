import asyncio
import discord
from discord.ext import commands
import json
import random

config = json.load(open('config.json'))
insults = []
turtle_quotes = []

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
    global turtle_quotes
    if not turtle_quotes:
        with open('turtle_quotes.txt') as f:
            turtle_quotes = f.read().splitlines()
    r = random.randint(0, len(turtle_quotes)-1)
    return turtle_quotes[r]


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def mkid(ctx):
    member = ctx.message.server.get_member(str(bot.user.id))
    await bot.change_nickname(member, "Turtle Quotes")
    message = get_mkid_quote();
    await bot.say(message)

@bot.command(pass_context=True)
async def quotes(ctx):
    member = ctx.message.server.get_member(str(bot.user.id))
    await bot.change_nickname(member, "Turtle Quotes")
    message = get_mkid_quote();
    await bot.say(message)



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
