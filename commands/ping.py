import config
from datetime import datetime
import time

def init():
    config.commands['ping'] = ping

async def ping(client, message):
    """checks bot latency"""
    tempPing = config.ping.microsecond - datetime.now().microsecond
    msg = await message.channel.send("Pong!")
    tempTime = datetime.now()
    tempPing = int((tempTime.microsecond - config.ping.microsecond) / 1000)
    tempPing += int(tempTime.second - config.ping.second) * 1000
    await msg.edit(content=f"Pong! {tempPing} ms")

if __name__ != '__main__':
    init()
