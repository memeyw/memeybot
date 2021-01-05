import config
import discord

def init():
    config.commands['source'] = postSource

async def postSource(client, message):
    """posts the source code link"""
    await message.channel.send("https://github.com/memeyw/memeybot")

if __name__ != '__main__':
    init()
