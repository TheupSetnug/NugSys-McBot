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