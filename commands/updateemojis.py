import config

def init():
    config.commands['updateemojis'] = updateEmojis

async def updateEmojis(client, message = ""):
    """updates bot's internal list of emojis"""
    config.emojis.clear()
    for guilds in client.guilds:
        for emoji in guilds.emojis:
            res, num = checkForDuplicate(emoji.name.lower())
            if (res):
                # if there is a duplicate, add new emoji + ## postfix or rename original if present
                if (emoji.name.lower() in config.emojis):
                    config.emojis[emoji.name.lower() + "2"] = ('<' + ('a' if emoji.animated else '') + ':' + emoji.name + ':' + str(emoji.id) + '>')
                    config.emojis[emoji.name.lower() + "1"] = config.emojis.pop(emoji.name.lower())
                else:
                    config.emojis[emoji.name.lower() + str(num).zfill(1)] = ('<' + ('a' if emoji.animated else '') + ':' + emoji.name + ':' + str(emoji.id) + '>')
            else:
                config.emojis[emoji.name.lower()] = ('<' + ('a' if emoji.animated else '') + ':' + emoji.name + ':' + str(emoji.id) + '>')

    if (not isinstance(message, str)):
        await message.channel.send('updated emoji list')

def checkForDuplicate(emoji):
    num = 1
    if emoji in config.emojis or emoji + "1" in config.emojis:
        #handle duplicate emoji names
        while (emoji + str(num).zfill(1) in config.emojis):
            num += 1
        return (True, num)
    else:
        return (False, num)

if __name__ != '__main__':
    init()
