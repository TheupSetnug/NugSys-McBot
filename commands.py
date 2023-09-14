#python script that contains all functions that translate user input into commands for the bot to execute

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command(name='help1')
async def help(ctx):
    await ctx.send('This is the help command')
    