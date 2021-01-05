import config
from datetime import datetime

def init():
    config.commands['uptime'] = uptime

async def uptime(client, message):
    """prints uptime"""
    current_time = datetime.now()
    elapsed_time = current_time - config.startTime
    await message.channel.send(str(elapsed_time.total_seconds()) + 's')

if __name__ != '__main__':
    init()
