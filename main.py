import botpy
import re
import yaml
import time
from botpy.message import Message
from botpy.logging import get_logger
from oj.codeforces import CF
import asyncio

_log = get_logger()

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

cf_channels = config['Codeforces']['Enable_channels']
cf_channels_remind = config['Codeforces']['Remind_channels']
print(cf_channels)
class jiangly_xcpc(botpy.Client):

    async def send_contest_reminder(self):
        while True:
            await CF.update()
            await CF.load_next_contest()
            next_contest = CF.next_contest_info
            if next_contest:
                note_time = next_contest['note_time']
                current_time = time.time()
                sleep_time = note_time - current_time
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                    for channel_id in cf_channels_remind:
                        # print ("🤗比赛快要开始了:\n{}".format(next_contest['info']))
                        _log.info("[botpy] send contest reminder to channel {}".format(channel_id))
                        await self.api.post_message(channel_id=channel_id, content="🤗比赛快要开始了:\n{}".format(next_contest['info']))
                    # await self.send_message(channel_id, content="比赛即将开始！")
                    # self.api.post_message(channel_id="xxxx", content="xxx", msg_id="xxxx", embed=embed)
            await asyncio.sleep(60 * 60)

    def run (self, appid, token):
        super().run(appid, token)

    def on_ready(self):
        asyncio.create_task(self.send_contest_reminder())
        
    async def on_message_create(self, message: Message):
        _log.info('[{}]在[{}] 说: {}'.format(message.author.username,message.channel_id, message.content))
        
        # ping
        if message.content is not None and re.match("^ping", message.content):
            await message.reply(content="pong")


        # codeforces
        if message.channel_id in cf_channels:
            if message.content is not None and re.match("下一场cf", message.content):
                _log.info('[{}]在[{}] 查询下一场codeforces时间'.format(message.author.username,message.channel_id))
                print(message)
                await CF.update()
                await CF.load_next_contest()
                msg = CF.next_contest_info['info']
                # print(CF)
                await message.reply(content=msg)

            if message.content is not None and re.match("近期cf", message.content):
                
                _log.info('[{}]在[{}] 查询近期codeforces时间'.format(message.author.username,message.channel_id))
                await CF.update()
                await CF.load_recent_contests()
                # print(CF)
                msg = ""
                for idx, contest in enumerate(CF.recent_contests_info):
                    msg += "" if idx == 0 else "\n\n"
                    msg += contest['info'] 
                await message.reply(content=msg)


    


CF = CF()
# print(CF.info)
intents = botpy.Intents(guild_messages=True)
client = jiangly_xcpc(intents=intents)
client.run(appid=config['qqbot']['appid'], token=config['qqbot']['token'])
