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
        authorName = message.author.name + '#' + message.author.discriminator
        authorId = message.author.id


        match commandType:

            case 'report':

                print('Create a Report')
                command = messageContent[8:].split(',')

                try:
                    if command[0] == "" or command[0] == "" or command[1] == "" or command[2] == "" or command[0] == None or command[1] == None or command[2] == None:
                        await message.channel.send('Malformed Request, please try again.')
                        return
                
                except:
                    await message.channel.send('An Error occurred, please try again.')
                params = {'reportedBy': authorName, 'reporterId': authorId, 'reportedName': command[0].strip().lower(), 'server': command[1].strip().lower(), 'cause': command[2].strip().lower(), 'commendation': 0}
                REPORTSURL = BASEURL + 'reports'

                requests.post(REPORTSURL, data=params)

                await message.channel.send(f'{command[0].strip().title()} reported due to: {command[2].strip()}')

            case 'commend':
                print('Create a Commendation')
                command = messageContent[8:].split(',')

                try:
                    if command[0] == "" or command[0] == "" or command[1] == "" or command[2] == "" or command[0] == None or command[1] == None or command[2] == None:
                        await message.channel.send('Malformed Request, please try again.')
                        return

                except:
                    await message.channel.send('An Error occurred, please try again.')

                params = {'reportedBy': authorName, 'reporterId': authorId, 'reportedName': command[0].strip().lower(), 'server': command[1].strip().lower(), 'cause': command[2].strip().lower(), 'commendation': 1}
                REPORTSURL = BASEURL + 'reports'
                requests.post(REPORTSURL, data=params)

                await message.channel.send(f'{command[0].strip().title()} commended due to: {command[2].strip()}')

            case 'check':
                print('Check Player')
                command = messageContent[7:].split(',')

                try:
                    if command[0] == "" or command[1] == "" or command[0] == None or command[1] == None:
                        await message.channel.send('Malformed Request, please try again.')
                        return

                except:
                    await message.channel.send('An error occurred, please try again.')

                params = {'playerName': command[0].strip().lower(), 'server': command[1].strip().lower()}
                PLAYERURL = BASEURL + 'player'
                response = requests.get(PLAYERURL, params)

                if response.ok:
                    player = response.json()
                    playerName = player.get('name')
                    server = player.get('server')
                    numberOfCommendations = player.get('numberOfCommendations')
                    numberOfReports = player.get('numberOfReports')

                    await message.channel.send(f'{playerName.title()} from {server.title()} server has {numberOfReports} reports and {numberOfCommendations} commendations.')

                else:
                    await message.channel.send(f'Error: {response.status_code}' )

            case 'help':
                await message.channel.send('The current functional commands are !report, !commend, and !check.  For !report and !commend, the format is as follows:  !command Player Name, Server, Cause for report.')
                await message.channel.send('For !check, the format is simply: !check Player Name, Server')

            case _ :
                await message.channel.send('Command was improperly formatted or missing.  Please try again.  If you don\'t know how to use this bot, try the !help command for instructions.')




client.run(TOKEN)
