
try:
    import configparser
    import sys
    import discord
    import shutil
except ImportError:
    print('Error importing required libraries, installing them now')
    try:
        import install
        install.install_required_libraries()
        import configparser
        import sys
        import discord
        import shutil
    except:
        print('Error importing required libraries, please install them manually')
        sys.exit(1)

intents = discord.Intents.all()
client  = discord.Client(intents=intents)

#define a function that prints a message to the debug channel

async def debug_message(message):
    DISCORD_TOKEN, DEBUG_CHANNEL_ID, GUILD_IDS, CHANNEL_IDS = load_config()
    #if the debug channel id is not set, print a warning and continue
    if DEBUG_CHANNEL_ID == '{}':
        print('WARNING: debug channel id not set, debug messages will not be sent')
    else:
        #send a message to the debug channel
        print('sending debug message to channel id: ' + DEBUG_CHANNEL_ID)
        channel = client.get_channel(int(DEBUG_CHANNEL_ID))
        await channel.send(message)

#check for config file called settings.conf, if not, copy the file called settings.conf.example to settings.conf
def load_config():
    #refresh every variable in the config file
    try:
        open('settings.conf')
        config = configparser.ConfigParser()
        config.read('settings.conf')
        DISCORD_TOKEN = config['DEFAULT']['DISCORD_TOKEN']
        DEBUG_CHANNEL_ID = config['DEFAULT']['DEBUG_CHANNEL_ID']
        GUILD_IDS = config['WHITELIST']['GUILD_IDS']
        CHANNEL_IDS = config['WHITELIST']['CHANNEL_IDS']
    except:
        print('Error opening settings.conf')

    return DISCORD_TOKEN, DEBUG_CHANNEL_ID, GUILD_IDS, CHANNEL_IDS

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
DEBUG_CHANNEL_ID = config['DEFAULT']['DEBUG_CHANNEL_ID']
JOURNALS = []

def load_journals():
    #if there is a section called [JOURNALS], add each comma separated item in [PARTS] to a list called JOURNALS
    try:
        PARTS = config['JOURNALS']['PARTS'].split(',')
        print('parts: ' + str(PARTS))
        #for each item in PARTS, use it to create a dictionary of journals by looking for a variable in [JOURNALS] called by the name of the item and getting a channel id from it
        for part in PARTS:
            JOURNALS.append({part: config['JOURNALS'][part]})
        print('journals: ' + str(JOURNALS))
        return JOURNALS
    except:
        print('No journals found in settings.conf, please add them to the [JOURNALS] section')
        return None
    
#load journals
JOURNALS = load_journals()

#if the debug channel id is not set, print a warning and continue
if DEBUG_CHANNEL_ID == '{}':
    print('WARNING: debug channel id not set, debug messages will not be sent')
else:
    print('debug channel id: ' + DEBUG_CHANNEL_ID)

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

@client.event
async def on_ready():
    #print the bot name and id when the bot is ready
    print('Logged in as {0.user}'.format(client))
    DISCORD_TOKEN, DEBUG_CHANNEL_ID, GUILD_IDS, CHANNEL_IDS = load_config()
    #print part of the discord token for debugging
    print('discord token: ' + DISCORD_TOKEN[:10] + '...')
    #print the debug channel id for debugging
    print('debug channel id: ' + DEBUG_CHANNEL_ID)
    #print the guild ids for debugging
    print('guild ids whitelisted: ' + GUILD_IDS)
    #print the channel ids for debugging
    print('channel ids whitelisted: ' + CHANNEL_IDS)
    await debug_message('Bot is ready')


@client.event
async def on_message(message):
    #if the message starts with !, ignore it
    if message.content.startswith('!'):
        return
    #if the message is in a channel that is one of the journals
    for journal in JOURNALS:
        for key, value in journal.items():
            if str(message.channel.id) == value:
                #if the message is from the bot, ignore it. else get the messages
                if message.author == client.user:
                    return
                print('message in journal, adding to master journal')
                created_at = message.created_at
                message_content = message.content
                #get the journal name for the message
                journal_name = key
                await debug_message(f'New Journal Entry from {journal_name}:```\n{message_content}\n```')
                break

    DISCORD_TOKEN, DEBUG_CHANNEL_ID, GUILD_IDS, CHANNEL_IDS = load_config()
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
    #send the message details to the debug channel
    await debug_message(message_details)
    
   
#start the bot
client.run(DISCORD_TOKEN)