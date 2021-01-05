import config

def init():
    config.commands['updateemojis'] = updateEmojis

async def updateEmojis(client, message = ""):
    """updates bot's internal list of emojis"""
    for guilds in client.guilds:
        if (guilds.id == 720894309095964753):
            guild = guilds
            for emoji in guilds.emojis:
                if (emoji.animated):
                    config.emojis[emoji.name.lower()] = ('<a:' + emoji.name + ':' + str(emoji.id) + '>')
                else:
                    config.emojis[emoji.name.lower()] = ('<:' + emoji.name + ':' + str(emoji.id) + '>')

    if (not isinstance(message, str)):
        await message.channel.send('updated emoji list')

if __name__ != '__main__':
    init()
