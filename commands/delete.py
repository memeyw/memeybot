import config

def init():
    config.commands['delete'] = deleteMsg

async def deleteMsg(client, message):
    """deletes the last posted bot message (only works for 1 use)"""
    await config.lastMessage.delete()

if __name__ != '__main__':
    init()
