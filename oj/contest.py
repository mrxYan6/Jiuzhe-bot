import abc
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time

class Contest(metaclass=abc.ABCMeta):

    def __init__(self):
        self.info = None
        self.begin_time = None
        self.during_time = None
        self.note_time = None
        self.end_time = None
        self.update_time = None
        self.cur_time = None
        # self.logger = logger

    async def initialize(self):
        # if(time)
        await self.update_local_contest()
        await self.load_next_contest()

    async def update_contest(self):
        if await self.update_local_contest():
            await self.load_next_contest()
            # self.logger.info('更新比赛成功!')
            print(1)
            return True
        else:
            # self.logger.info('更新比赛失败!')
            print(0)
            return False

    @abc.abstractmethod
    async def get_next_contest(self):
        pass

    @abc.abstractmethod
    async def update_local_contest(self):
        pass

    @abc.abstractmethod
    async def get_contest_info(self):
        pass

    async def load_next_contest(self):
        self.info, self.begin_time, self.during_time = await self.get_next_contest()
        self.note_time = self.begin_time - 15 * 60
        self.end_time = self.begin_time + self.during_time
        self.update_time = self.end_time + 10 * 60
