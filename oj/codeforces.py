import abc
import time
import json
from mytools.web import *

from botpy.logging import get_logger
_log = get_logger()
class Contest(metaclass=abc.ABCMeta):

    def __init__(self):
        self.info = None
        self.begin_time = None
        self.during_time = None
        self.note_time = None
        self.end_time = None
        self.update_time = 0
        self.recent_contests_info = []
        self.next_contest_info = {}


    def __str__(self) -> str:
        """Return a string representation of the object."""
        return "contests:{}, next_contest:{}, recent_contests:{}".format(
            self.info, self.next_contest_info, self.recent_contests_info)
       
    async def update(self):
        if(time.time() > self.update_time):
            if await self.update_local_contest():
                self.update_time = time.time() + 60 * 3
            else:
                Exception("Update local contest failed!")
            if await self.load_next_contest():
                return True
            else:
                Exception("Load next contest failed!")
        else:
            return True

    async def load_next_contest(self):
        info, begin_time, during_time = await self.get_next_contest()
        if info:
            self.next_contest_info = {
                'info': info,
                'begin_time': begin_time,
                'during_time': during_time,
                'note_time': begin_time - 15 * 60,
                # 'note_time': time.time() + 20,
                'end_time': begin_time + during_time
            }
            return True
        else:
            return False

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
            return True
        else:
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

    @abc.abstractmethod
    async def get_recent_contests(self):
        pass


class CF(Contest):
    async def update_local_contest(self):
        url = "https://codeforces.com/api/contest.list?gym=false"
        try:
            json_data = await get_json(url)
            if json_data:
                with open('./oj_json/cf_contest.json', 'w') as f:
                    json.dump(json_data, f)
                return True
            else:
                return False
        except Exception as e:
            _log.error(f"[codeforces] Error: {e}")
            return False

    async def get_contest(self):
        try:
            with open('./oj_json/cf_contest.json', 'r') as f:
                json_data = json.load(f)
            if json_data:
                contest_list_all = list(json_data['result'])
                contest_list_lately = [contest for contest in contest_list_all if contest['relativeTimeSeconds'] < 0 and contest['name'][:6] != 'Kotlin' and 'Unrated' not in contest['name']]
                if contest_list_lately:
                    contest_list_lately.sort(key=lambda x: (x['relativeTimeSeconds'], x['name']), reverse=True)
                return contest_list_lately
            else:
                return []
        except Exception as e:
            _log.error(f"[codeforces] Error: {e}")
            return []

    async def format_cf_contest(self, contest):
        return "🤪Name: {}\n🥵Start: {}\n🤤Length: {}".format(
            contest['name'],
            time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(int(contest['startTimeSeconds']))),
            "{:02d}:{:02d}".format(
                contest['durationSeconds'] // 3600, contest['durationSeconds'] % 3600 // 60)
        )

    async def get_next_contest(self):
        contest_list_lately = await self.get_contest()
        if not contest_list_lately:
            return None, None, None
        else:
            for contest in contest_list_lately:
                res = await self.format_cf_contest(contest)
                return res, int(contest['startTimeSeconds']), int(contest['durationSeconds'])

    async def get_recent_contests(self):
        contest_list_lately = await self.get_contest()
        if not contest_list_lately:
            return None
        else:
            contest_list = []
            for contest in contest_list_lately:
                res = await self.format_cf_contest(contest)
                contest_list.append((res, int(contest['startTimeSeconds']), int(contest['durationSeconds'])))
            return contest_list

    async def get_contest_info(self, contest_id):
        url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}"
        json_data = await get_json(url)
        if json_data:
            return json_data['result']
        else:
            return None
