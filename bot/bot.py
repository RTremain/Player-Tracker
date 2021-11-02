# bot.py
import os
import threading
import asyncio
import random
import time
import requests
import requests_cache
import pathlib

import discord
import logging, logging.handlers

from discord import channel
from discord.ext import commands
from dotenv import load_dotenv


requests_cache.install_cache('api_requests_cache', backend='sqlite', expire_after=180)


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('../logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client();

BASEURL = "http://localhost:5000/api/"


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return


    # Messages should start with ! to signify a command.

    if message.content.startswith('!'):
        messageContent = message.content
        commandType = message.content[1:].split(' ')[0]



        match commandType:
            case 'report':
                print('Create a Report')
                command = messageContent[8:].split(',')
                print(command[0].strip())
                print(command[1].strip())
                print(command[2].strip())
                params = {'reportedBy': 'testName', 'reportedName': command[0].strip(), 'server': command[1].strip(), 'cause': command[2].strip(), 'commendation': 0}
                print(params)
                REPORTSURL = BASEURL + 'reports'
                requests.post(REPORTSURL, data=params)
                await message.channel.send(f'{command[0].strip()} reported due to: {command[2].strip()}')
            case 'commend':
                print('Create a Commendation')
                command = messageContent[8:].split(',')
                print(command[0].strip())
                print(command[1].strip())
                print(command[2].strip())
                if command[0] == "" | command[1] == "" | command[2] == "":
                    await message.channel.send('Malformed Request, please try again.')
                params = {'reportedBy': 'testName', 'reportedName': command[0].strip(), 'server': command[1].strip(), 'cause': command[2].strip(), 'commendation': 1}
                print(params)
                REPORTSURL = BASEURL + 'reports'
                requests.post(REPORTSURL, data=params)
                await message.channel.send(f'{command[0].strip()} commended due to: {command[2].strip()}')
            case 'check':
                print('Check Player')
                command = messageContent[7:].split(',')
                print(command[0].strip())
                print(command[1].strip())

                params = {'playerName': command[0].strip(), 'server': command[1].strip()}

                PLAYERURL = BASEURL + 'player'

                player = requests.get(PLAYERURL, params).json()

                playerName = player.get('name')

                server = player.get('server')

                numberOfCommendations = player.get('numberOfCommendations')

                numberOfReports = player.get('numberOfReports')

                await message.channel.send(f'{playerName} from {server} server has {numberOfReports} reports and {numberOfCommendations} commendations.')
            case 'help':
                await message.channel.send('The current functional commands are !report, !commend, and !check.  For !report and !commend, the format is as follows:  !command Player Name, Server, Cause for report.')
                await message.channel.send('For !check, the format is simply: !check Player Name, Server')
            case _:
                await message.channel.send('Command was improperly formatted or missing.  Please try again.  If you don\'t know how to use this bot, try the !help command for instructions.')




client.run(TOKEN)
