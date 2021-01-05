from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import random
import xml.etree.ElementTree as ET
import aiohttp
from re import sub
import discord

import config

def init():
    config.commands['g'] = gelbooru
    config.commands['gp'] = gelbooru

async def gelbooru(client, message):
    #TODO: Remove discord integration from this module
    """searches gelbooru (g sfw, gp nsfw)"""
    messageTxt = message.content.split(" ")
    del messageTxt[0]

    tagsList = ""
    searchLink = 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=50&sort:random&tags='
    if (messageTxt[0] == "g"):
        searchLink += "rating:safe "
    elif (messageTxt[0] == "gp"):
        searchLink += "-rating:safe "
    del messageTxt[0]

    for tags in messageTxt:
        tagsList += tags + " "
        searchLink += tags + " "
    searchLink += '&api_key=a1bf7aba97524a2b7df1c86d011d927c66c34cb1071c970f4c95b11c66e955a6&user_id=690473'

    async with aiohttp.ClientSession() as session:
        async with session.get(searchLink) as response:
            root = ET.fromstring(await response.text())

    try:
        result = random.choice(root)
    except IndexError:
        await message.channel.send("No images found for " + tagsList)
        return

    file_url = result.get('file_url')
    id = result.get('id')
    characterMsg = ""
    print(id)

    async with aiohttp.ClientSession() as session:
        async with session.get('https://gelbooru.com/index.php?page=post&s=view&id=' + id) as response:
            root = await response.text()

    only_tags_with_character = SoupStrainer('li', {'class' : 'tag-type-character'})
    parsedHtml = BeautifulSoup(root, 'lxml', parse_only=only_tags_with_character)
    try:
        characters = parsedHtml.select('.tag-type-character')
    except AttributeError:
        pass

    if (not characters):
        characterMsg = "None"
    else:
        for character in characters:
            characterMsg += sub(r'\d+', '', character.text.replace('?', '')) + "\n"

    resultEmbed = discord.Embed(title="", description="", color=0x773c8f)
    resultEmbed.add_field(name="characters", value=characterMsg, inline=False)
    if (".mp4" in file_url):
        await message.channel.send(embed=resultEmbed)
        await message.channel.send(file_url)
        return
    else:
        resultEmbed.set_image(url=file_url)

    print(searchLink)
    await message.channel.send(embed=resultEmbed)

if __name__ != "__main__":
    init()
