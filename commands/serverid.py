import config

def init():
    config.commands['serverid'] = serverID

async def serverID(client, message):
    """returns the server id"""
    await message.channel.send(message.guild.id)

if __name__ != '__main__':
    init()
