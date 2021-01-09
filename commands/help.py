import config

def init():
    config.commands['help'] = helpFancy

async def helpFancy(client, message):
    #TODO: Remove discord integration
    """shows all commands"""
    sentMsg = await message.channel.send(embed=config.helpPages[0])
    await sentMsg.add_reaction('⬅️')
    await sentMsg.add_reaction('➡️')

if __name__ != '__main__':
    init()
