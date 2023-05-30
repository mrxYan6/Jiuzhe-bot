import abc
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import time
from typing import Any, Dict, List, Tuple, Union

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

    async def initialize(self) -> Union[bool, str]:
        if time.time() > self.update_time:
            ret = await self.update_contest()
            if ret == 'successful':
                return True
            else:
                return ret
        else:
            return 'initialize failed'

    async def update_contest(self) -> str:
        if await self.initialize():
            if await self.load_next_contest() == 'successful':
                return 'successful'
            return 'load next contest failed'
        else:
            return 'initialize failed'

    @abc.abstractmethod
    async def get_next_contest(self) -> Tuple[str, int, int]:
        pass

    @abc.abstractmethod
    async def update_local_contest(self) -> str:
        pass

    @abc.abstractmethod
    async def get_contest_info(self) -> Any:
        pass

    @abc.abstractmethod
    async def get_recent_contests(self) -> List[Tuple[str, int, int]]:
        pass

    async def load_next_contest(self) -> str:
        info, begin_time, during_time = await self.get_next_contest()
        if info:
            self.next_contest_info = self.create_contest_info(info, begin_time, during_time)
            self.update_time = self.next_contest_info['end_time'] + 10 * 60
            return 'successful'
        else:
            return 'load next contest failed'

    async def load_recent_contests(self) -> str:
        recent_contests = await self.get_recent_contests()
        if recent_contests:
            self.recent_contests_info = [self.create_contest_info(*contest) for contest in recent_contests]
            return 'successful'
        else:
            return 'load recent contestsfailed'

    @staticmethod
    def create_contest_info(info: str, begin_time: int, during_time: int) -> Dict[str, Union[str, int]]:
        return {
            'info': info,
            'begin_time': begin_time,
            'during_time': during_time,
            'note_time': begin_time - 15 * 60,
            'end_time': begin_time + during_time
        }
