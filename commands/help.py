import config

def init():
    config.commands['help'] = help
    config.commands['helpf'] = helpFancy

async def help(client, message):
    """shows all commands in plaintext"""
    helpMsg = ""
    for entry in config.helpPlaintext:
        helpMsg += config.helpPlaintext[entry] + "\n"

    await message.channel.send(helpMsg)

async def helpFancy(client, message):
    #TODO: Remove discord integration
    """shows all commands, fancy"""
    sentMsg = await message.channel.send(embed=config.helpPages[0])
    await sentMsg.add_reaction('⬅️')
    await sentMsg.add_reaction('➡️')

if __name__ != '__main__':
    init()
