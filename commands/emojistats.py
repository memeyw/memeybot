import config
import discord
import sqlite3
import asyncio
import sqlhelpers
from commands import updateemojis

def init():
    config.commands['stats'] = emojiStats
    config.commands['clearstats'] = clearStats
    config.commands['rmstat'] = removeStat

async def emojiStats(client, message):
    """view emoji usage stats"""
    dict = {}

    con = sqlhelpers.connectToDB(config.emojiDBPath + 'stats' + config.commandPrefix + str(message.guild.id) + ".db")
    con.row_factory = sqlhelpers.dict_factory
    cursor = con.cursor()

    sqlhelpers.checkForTable('emotes', message.guild.id)
    cursor.execute('select * from emotes order by cast(timesUsed as int) desc')

    data = cursor.fetchall()
    msg = ''
    await updateemojis.updateEmojis(client)
    for dict in data:
        cursor.execute("select emoteName from emotes where emoteName = ?", (dict["emoteName"],))
        data = cursor.fetchall()
        if (dict["emoteName"] not in config.emojis.values()):
            newName = dict["emoteName"].split(':')[1] + '~deleted'
            msg += newName + " - " + str(dict["timesUsed"]) + "\n"
            cursor.execute("update emotes set emoteName = ? where emoteName = ?", (newName,dict["emoteName"]))
            con.commit()
        else:
            msg += dict["emoteName"] + " - " + str(dict["timesUsed"]) + "\n"
    await message.channel.send("No stats found. Get to work!" if msg == '' else msg)

async def clearStats(client, message):
    """clears emoji usage stats"""
    await message.channel.send("Are you sure you want to clear stats? y/n")

    def check(msg):
        return msg.content.lower() in ['y', 'n'] and msg.channel == message.channel

    try:
        msg = await client.wait_for('message', timeout=15.0, check=check)
        if (msg.content.lower() == 'y'):
            con = sqlhelpers.connectToDB(config.emojiDBPath + 'stats' + config.commandPrefix + str(message.guild.id) + ".db")
            cursor = con.cursor()
            cursor.execute('delete from emotes')
            con.commit()
            await message.channel.send("Stats cleared.")
        elif (msg.content.lower() == 'n'):
            await message.channel.send("Clear stats request cancelled.")
    except asyncio.TimeoutError:
        await message.channel.send("Clear stats request timed out.")

async def removeStat(client, message):
    """clears emoji usage stats"""
    params = message.content.replace("{} ".format(config.commandPrefix), '').split(" ")
    del params[0]
    if (len(params) == 0):
        await message.channel.send("Please specify stats to remove.")
        return
    await message.channel.send("Are you sure you want to remove " + ", ".join(params) + "? y/n")

    def check(msg):
        return msg.content.lower() in ['y', 'n'] and msg.channel == message.channel

    try:
        msg = await client.wait_for('message', timeout=15.0, check=check)
        if (msg.content.lower() == 'y'):
            con = sqlhelpers.connectToDB(config.emojiDBPath + 'stats' + config.commandPrefix + str(message.guild.id) + ".db")
            cursor = con.cursor()
            notFound = []
            for param in params:
                cursor.execute("select emoteName from emotes where emoteName = ?", (param,))
                data = cursor.fetchall()
                if not data:
                    notFound.append(param)
                else:
                    cursor.execute('delete from emotes where emoteName=?', (param,))
                    con.commit()
            if (len(notFound) == len(params)):
                await message.channel.send("Stat(s) " + ", ".join([missing for missing in notFound]) + " not found.")
            elif (len(notFound) != 0):
                await message.channel.send("Stat(s) " + ", ".join([missing for missing in notFound]) + " not found.")
                await message.channel.send("Stats removed.")
            else:
                await message.channel.send("Stats removed.")
        elif (msg.content.lower() == 'n'):
            await message.channel.send("Remove stats request cancelled.")
    except asyncio.TimeoutError:
        await message.channel.send("Remove stats request timed out.")

if __name__ != '__main__':
    init()
