import botpy

import yaml
from botpy.message import Message,DirectMessage
from botpy.logging import get_logger
_log = get_logger()

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

class Private(botpy.Client):
    async def on_message_create(self, message: Message):
        # print(message)
        _log.info('[{}] 说: {}'.format(message.author.username,message.content))
        if(message.content!=None and message.content.__contains__("ping")):
            msg = await message.reply(content="pong")
            _log.info(msg=msg)
        # print('[{}] 说: '.format(message.author.username),message.content)
    async def on_message_delete(self, message: Message):
        _log.info('[{}] 删除了一条消息'.format(message.author.username))
        

intents = botpy.Intents(guild_messages=True) 
client = Private(intents=intents)
client.run(appid=config['qqbot']['appid'], token=config['qqbot']['token'])
