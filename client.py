import configparser
import sys
import discord
from discord.ext import commands
import shutil

intents = discord.Intents.all()
client  = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents)

#check for config file called settings.conf, if not, copy the file called settings.conf.example to settings.conf
def load_config():
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

    #set variables from config file
    DISCORD_TOKEN = config['DEFAULT']['DISCORD_TOKEN']

    #read settings.conf under the [WHITELIST] for GUILD_IDS={} and CHANNEL_IDS={} and set them to variables
    #if there are is no [WHITELIST] section in the config file, add it
    if 'WHITELIST' not in config:
        config['WHITELIST'] = {}
        config['WHITELIST']['GUILD_IDS'] = '{}'
        config['WHITELIST']['CHANNEL_IDS'] = '{}'
        with open('settings.conf', 'w') as configfile:
            config.write(configfile)
        print('Please edit settings.conf with your guild and channel ids')
        sys.exit(1)
    #if the guild or channel ids are not set, exit the script
    if config['WHITELIST']['GUILD_IDS'] == '{}' or config['WHITELIST']['CHANNEL_IDS'] == '{}':
        print('Please edit settings.conf with your guild and channel ids')
        sys.exit(1)
    GUILD_IDS = config['WHITELIST']['GUILD_IDS']
    CHANNEL_IDS = config['WHITELIST']['CHANNEL_IDS']
    return DISCORD_TOKEN, GUILD_IDS, CHANNEL_IDS

DISCORD_TOKEN, GUILD_IDS, CHANNEL_IDS = load_config()

@bot.command(name='!addchannel', help='Add a channel to the whitelist')
async def addchannel(ctx):
    #check to see if the guild id is in the whitelist, if not, ignore the message
    if str(ctx.guild.id) not in GUILD_IDS:
        print(f'guild id {ctx.guild.id} not in whitelist')
        return
    #get the channel id and add it to the config file unless it is already in the config file
    channel_id = ctx.channel.id
    if str(channel_id) in CHANNEL_IDS:
        await ctx.send('Channel already in whitelist')
        return 
    else:
        config = configparser.ConfigParser()
        config.read('settings.conf')
        config['WHITELIST']['CHANNEL_IDS'] = CHANNEL_IDS + ',' + str(channel_id)
        with open('settings.conf', 'w') as configfile:
            config.write(configfile)
        await ctx.send('Channel added to whitelist')

@client.event
async def on_ready():
    #print the bot name and id when the bot is ready
    print('Logged in as {0.user}'.format(client))
    DISCORD_TOKEN, GUILD_IDS, CHANNEL_IDS = load_config()
    #print part of the discord token for debugging
    print('discord token: ' + DISCORD_TOKEN[:10] + '...')
    #print the guild ids for debugging
    print('guild ids whitelisted: ' + GUILD_IDS)
    #print the channel ids for debugging
    print('channel ids whitelisted: ' + CHANNEL_IDS)

@client.event
async def on_message(message):
    #if the message starts with !, ignore it
    if message.content.startswith('!'):
        return
    DISCORD_TOKEN, GUILD_IDS, CHANNEL_IDS = load_config()
    #check to see if the guild id is in the whitelist, if not, ignore the message
    if str(message.guild.id) not in GUILD_IDS:
        print(f'guild id {message.guild.id} not in whitelist')
        return
    #check to see if the channel id is in the whitelist, if not, ignore the message
    if str(message.channel.id) not in CHANNEL_IDS:
        print(f'channel id {message.channel.id} not in whitelist')
        return
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