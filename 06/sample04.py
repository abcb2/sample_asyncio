import re
import os
import time
from datetime import datetime as dt


def match():
    d = '2018-03-28 18:00:00.12345 +09:00'
    m = re.search(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}).+$", d)
    if m:
        print(m.groups())
        print(m.group(1))

def diff():
    d = '2018-03-28 18:00:00'
    dp1 = dt.strptime(d, "%Y-%m-%d %H:%M:%S")

    dnow = dt.now()
    print(type(dp1))
    print(type(dnow))

    diff = dnow - dp1
    print(type(diff))
    print(diff)
    print(diff.total_seconds())

def my_stat():
    mtime = os.stat("./sample01.py").st_mtime
    d = dt.fromtimestamp(mtime)
    print(dt.strftime(d, "%Y-%m-%d %H:%M:%S"))
    # ret = time.mktime(time.localtime(mtime))
    # print(type(ret))
    # print(ret)
    # print(dt.strftime(ret, "%Y-%m-%d %H:%M:%S"))

my_stat()

# s = "hoge"
# b = b"1234-hoge"
#
# if re.match(r'^\d{4}-', b.decode('utf-8')):
#     print(100)
# else:
#     print(200)