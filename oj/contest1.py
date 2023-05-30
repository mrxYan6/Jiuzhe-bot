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
        self.update_time = 0
        self.cur_time = None
        # self.logger = logger

    async def initialize(self):
        if(time.time() > self.update_time):
            ret = await self.update_contest()
            if ret == 'successful':
                return True
            else:
                return ret
        else:
            return 'initialize failed'

    async def update_contest(self):
        if await self.initialize():
            if await self.load_next_contest():
                return 'successful'
            return 'load next contest failed'
        else:
            return 'initialize failed'

    

    async def load_next_contest(self):
        info, begin_time, during_time = await self.get_next_contest()
        if info:
            self.next_contest_info = {
                'info': info,
                'begin_time': begin_time,
                'during_time': during_time,
                'note_time': begin_time - 15 * 60,
                'end_time': begin_time + during_time
            }
            self.update_time = self.next_contest_info['end_time'] + 10 * 60
            return 'successful'
        else:
            return 'load next contest failed'


    async def load_recent_contests(self):
        recent_contests = await self.get_recent_contests()
        if recent_contests:
            self.recent_contests_info = []
            for contest in recent_contests:
                contest_info = {
                    'info': contest[0],
                    'begin_time': contest[1],
                    'during_time': contest[2],
                    'note_time': contest[1] - 15 * 60,
                    'end_time': contest[1] + contest[2]
                }
                self.recent_contests_info.append(contest_info)
            return 'successful'
        else:
            return 'load recent contests failed'
        

    @abc.abstractmethod
    async def get_next_contest(self):
        pass

    @abc.abstractmethod
    async def update_local_contest(self):
        pass

    @abc.abstractmethod
    async def get_contest_info(self):
        pass

    @abc.abstractmethod
    async def get_recent_contests(self):
        pass