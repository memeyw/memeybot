import aiohttp
import config

from discord import errors

def init():
    config.commands['changepfp'] = changePfp

async def changePfp(client, message):
    #TODO: ADD ABILITY TO SELECT USER
    """changes nickname and pfp to a specified @user (requesting user if none specified, kinda borked atm)"""
    messageTxt = message.content.split(" ")
    del messageTxt[0]

    try:
        #change back to default nick/pfp
        if (len(messageTxt) > 1 and (messageTxt[1] == 'default')):
            if (config.commandPrefix == ';md'):
                with open(r'../bot icon dev.png', 'rb') as f:
                    image = f.read()
            else:
                with open(r'../botto icon.png', 'rb') as f:
                    image = f.read()
            await client.user.edit(avatar=image)
            nick = await message.guild.me.edit(nick='memey')
            await message.channel.send('changed back to default pfp and nickname')
        #mentioned user's nick/pfp
        elif (len(messageTxt) > 1):
            await message.delete()
            if (message.mentions[0].nick):
                await message.guild.me.edit(nick=message.mentions[0].nick)
            else:
                await message.guild.me.edit(nick=message.mentions[0].display_name)
            async with aiohttp.ClientSession() as session:
                async with session.get(str(message.mentions[0].avatar_url)) as response:
                    html = await response.read()
                    await client.user.edit(avatar=html)
        #message author's nick/pfp
        else:
            await message.delete()
            if (message.author.nick):
                await message.guild.me.edit(nick=message.author.nick)
            else:
                await message.guild.me.edit(nick=message.author.display_name)
            async with aiohttp.ClientSession() as session:
                async with session.get(str(message.author.avatar_url)) as response:
                    html = await response.read()
                    await client.user.edit(avatar=html)
    except Exception as e:
        print(e)
        await message.channel.send('discord timeout error')
        return

if __name__ != '__main__':
    init()
