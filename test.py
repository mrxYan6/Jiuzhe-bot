import botpy
import re
import yaml
from botpy.message import Message
from botpy.logging import get_logger
from oj.codeforces import CF
import asyncio

CF = CF()

print(asyncio.run(CF.load_recent_contests()))
print(asyncio.run(CF.load_next_contest()))
print(CF)