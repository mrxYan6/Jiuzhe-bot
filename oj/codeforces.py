import sys
sys.path.append('/home/mrx/code/robot/QQbot/Jiuzhe-bot/')
import json
import sys
import time
from mytools.web import *
from oj.contest import Contest

import tracemalloc
tracemalloc.start()


class cf(Contest):
    async def update_local_contest(self):
        url = "https://codeforces.com/api/contest.list?gym=false"
        json_data = await get_json(url)
        if json_data == -1:
            return False
        json_data = dict(json_data)
        if json_data['status'] == "OK":
            with open('./oj_json/cf_contest.json', 'w') as f:
                json.dump(json_data, f)
        return True
    

    async def get_contest(self):
        with open('./oj_json/cf_contest.json', 'r') as f:
            json_data = json.load(f)
        if json_data == []:
            return []
        contest_list_all = list(json_data['result'])
        contest_list_lately = []

        for contest in contest_list_all:
            if contest['relativeTimeSeconds'] < 0:
                if contest['name'][:6] != 'Kotlin':
                    if 'Unrated' not in contest['name']:
                        contest_list_lately.append(contest)
            else:
                break
        if contest_list_lately:
            contest_list_lately.sort(key=lambda x: (
                x['relativeTimeSeconds'], x['name']), reverse=True)
        return contest_list_lately
    
    async def format_cf_contest(self, contest):
        contest_url = "https://codeforces.com/contest/"
        return "Name: {}\n\rStart: {}\n\rLength: {}".format(
            contest['name'],
            time.strftime("%Y-%m-%d %H:%M:%S",
                          time.localtime(int(contest['startTimeSeconds']))),
            "{:02d}:{:02d}".format(
                contest['durationSeconds'] // 3600, contest['durationSeconds'] % 3600 // 60)
        )


    async def get_next_contest(self):
        contest_list_lately = await self.get_contest()
        if not contest_list_lately:
            return "最近没有比赛", 32536700000, 0
        else:
            for contest in contest_list_lately:
                res = await self.format_cf_contest(contest)
                return res, int(contest['startTimeSeconds']), int(contest['durationSeconds'])

    async def get_contest_info(self, contest_id):
        # TODO: 根据比赛 ID 获取比赛详情信息
        pass