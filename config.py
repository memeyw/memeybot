import os

ping = 0
commands, helpPages, emojis, lastMessage = {}, {}, {}, {}
commandPrefix, emojiPrefix, startTime = '', '', ''
emojiDBPath = os.path.join(os.getcwd(), "stats", "")

print(emojiDBPath)
