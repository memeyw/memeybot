import discord
import aiohttp
import io
from datetime import datetime
import math
import lxml
import re
import os
import sys
import glob

import config
from commands import *

#globals
CLIENT = discord.Client()

def init():
    #Environment variables
    TOKEN = os.getenv('memeytoken')
    config.commandPrefix = ';m'

    if (sys.argv[1] == "dev"):
        TOKEN = os.getenv('memeydevtoken')
        config.commandPrefix = ';md'

    config.emojiPrefix = config.commandPrefix + 'e'
    config.startTime = datetime.now()
    CLIENT.run(TOKEN)

@CLIENT.event
async def on_ready():
    print('We have logged in as {0.user}'.format(CLIENT))
    await updateemojis.updateEmojis(CLIENT)
    print('Emojis updated')
    generateHelp()
    print('Help generated')

@CLIENT.event
async def on_message(message):
    if (message.author) == CLIENT.user:
        config.lastMessage = message
        return

    command = message.content.split(" ")
    if command[0] == config.commandPrefix:
        del command[0]

        try:
            await config.commands[command[0].lower()](CLIENT, message)
        except KeyError as k:
            await message.channel.send('command not found')
    elif command[0] == config.emojiPrefix:
        del command[0]

        try:
            await message.channel.send(numOfEmojis(command, len(command)))
        except KeyError:
            await message.channel.send('emoji(s) not found')

@CLIENT.event
async def on_raw_reaction_remove(payload):
    if (payload.user_id == CLIENT.user.id):
        return

    channel = CLIENT.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if (message.author != CLIENT.user):
        return

    currentPage = int(message.embeds[0].title[-3:-2])

    if ((payload.emoji.name == '➡️') and (currentPage < math.ceil((len(config.commands) + 1 ) / 4))):
        await message.edit(embed=config.helpPages[int(currentPage)])
    elif ((payload.emoji.name == '⬅️') and (currentPage != 1)):
        await message.edit(embed=config.helpPages[currentPage - 2])

@CLIENT.event
async def on_raw_reaction_add(payload):
    if (payload.user_id == CLIENT.user.id):
        return

    channel = CLIENT.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if (message.author != CLIENT.user):
        return

    currentPage = int(message.embeds[0].title[-3:-1].replace('/', ''))

    if ((payload.emoji.name == '➡️') and (currentPage < math.ceil((len(config.commands) + 1 ) / 4))):
        await message.edit(embed=config.helpPages[int(currentPage)])
    elif ((payload.emoji.name == '⬅️') and (currentPage != 1)):
        await message.edit(embed=config.helpPages[currentPage - 2])

#commands

async def addReactions(reaction):
    await sentMsg.add_reaction('⬅️')
    await sentMsg.add_reaction('➡️')

async def sendMessage(message):
    await message.channel.send(message)

async def sendMessageEmbed(message):
    await message.channel.send(message)

#internal commands

def generateHelp():
    pageNum = 0
    currentCommand = 1
    totalCommands = len(config.commands) + 1
    for x in range(totalCommands):
        config.helpPages[x] = discord.Embed(title="Commands {}/{}".format(x + 1, math.ceil(totalCommands / 4)), description="**usage:** " + config.commandPrefix + " <command> " + config.emojiPrefix + " <emoji name>", color=0x773c8f)

    for key in config.commands:
        if (currentCommand == 4):
            pageNum += 1
            currentCommand = 0

        config.helpPages[pageNum].add_field(name=key, value=config.commands[key].__doc__, inline=False)
        currentCommand += 1

def numOfEmojis(command, size):
    returnText = ''
    for x in range(size):
        returnText += config.emojis[command[x].lower()]

    return returnText

init()
