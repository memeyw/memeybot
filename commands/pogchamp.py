import config
import discord

def init():
    config.commands['pog'] = pogchamp

async def pogchamp(client, message):
    """poggies"""
    await message.channel.send("Ugh fine, I guess you are my little pogchamp, {}. Come here <:huggi:779783939002073100>".format(message.author.mention))

if __name__ != '__main__':
    init()
