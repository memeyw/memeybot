import config, glob, os, random
import discord

cats = []

def init():
    config.commands['meow'] = postCat
    os.chdir("./cats")
    for file in glob.glob("*.jpg"):
        cats.append(file)

async def postCat(client, message):
    """posts a cute meowster in the chat"""
    randIndex = random.randrange(len(cats))
    await message.channel.send(file=discord.File(cats[randIndex]))

if __name__ != '__main__':
    init()
