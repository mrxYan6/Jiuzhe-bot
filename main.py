import botpy
import re
import yaml
from botpy.message import Message
from botpy.logging import get_logger
from oj.codeforces import cf
import asyncio

_log = get_logger()

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

class Private(botpy.Client):
    async def on_message_create(self, message: Message):
        if message.content is not None and "/ping" in message.content:
            await message.reply(content="pong")



class jiangly_xcpc(botpy.Client):
    async def on_message_create(self, message: Message):
        _log.info('[{}]在[{}] 说: {}'.format(message.author.username,message.channel_id, message.content))
        if message.channel_id == '9312047' or message.channel_id == '391225439':
            if message.content is not None and re.match("下一场cf", message.content):
                _log.info('[{}]在[{}] 查询下一场codeforces时间'.format(message.author.username,message.channel_id))
                print(message)
                await CF.initialize()
                msg = CF.info
                await message.reply(content=msg)

    


CF = cf()
# print(CF.info)
intents = botpy.Intents(guild_messages=True)
client = jiangly_xcpc(intents=intents)
client.run(appid=config['qqbot']['appid'], token=config['qqbot']['token'])
