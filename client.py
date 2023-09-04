import configparser
import sys
import discord
import shutil

#check for config file called settings.conf, if not, copy the file called settings.conf.example to settings.conf
try:
    open('settings.conf')
except FileNotFoundError:
    print('No config file found, copying example config file to settings.conf/nPlease edit settings.conf with your bot token and other settings')
    try:
        shutil.copyfile('settings.conf.example', 'settings.conf')
    except:
        print('Error copying example config file to settings.conf')
        sys.exit(1)
except:
    print('Error opening settings.conf')
    sys.exit(1)
    
#read config file
config = configparser.ConfigParser()
config.read('settings.conf')

#for each variable in the default section in the config file, print each variable
for key in config['DEFAULT']:
    print(key + ': ' + config['DEFAULT'][key])

#set variables from config file
DISCORD_TOKEN = config['DEFAULT']['DISCORD_TOKEN']

#set intents to allow the bot to read messages
intents = discord.Intents.all()

#set the client to the discord bot
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    #if the message is from the bot, ignore it. else get the messages
    if message.author == client.user:
        return
    #get the details of the message
    message_content = message.content
    if message.guild:
        guild = message.guild.name
        channel = message.channel.name
    else:
        guild = None
        channel = None
    author = message.author.name
    # if the message is directed at the bot, get the mentions, of not return none
    if message.mentions:
        mentions = message.mentions
    else:
        mentions = None
    #get even more details
    created_at = message.created_at
    edited_at = message.edited_at
    if message.attachments:
        attachments = message.attachments
    else:
        attachments = None
    if message.reactions:
        reactions = message.reactions
    else:
        reactions = None
    #compile each of the message details into a dictionart and load it into a json file
    message_details = {
        "message_content": message_content,
        "guild": guild,
        "channel": channel,
        "author": author,
        "mentions": mentions,
        "created_at": created_at,
        "edited_at": edited_at,
        "attachments": attachments,
        "reactions": reactions
    }
    print(message_details)
    #send a response to the message
    response = 'Hello ' + author + ', you said: ' + message_content
    await message.channel.send(response)
   
#start the bot
client.run(DISCORD_TOKEN)