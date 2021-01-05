import config

def init():
    config.commands['parrot'] = parrot
    config.commands['parrotd'] = parrotDel

async def parrot(client, message):
    """Reposts message text"""
    messageTxt = message.content.replace(';md ', '')[6:]
    await message.channel.send(messageTxt)

async def parrotDel(client, message):
    """Reposts message text and deletes original msg"""
    messageTxt = message.content.replace(' parrotdel ', '').replace(config.commandPrefix, '')
    await message.channel.send(messageTxt)
    await message.delete()

if __name__ != '__main__':
    init()
