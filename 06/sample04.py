import re
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

diff()

# s = "hoge"
# b = b"1234-hoge"
#
# if re.match(r'^\d{4}-', b.decode('utf-8')):
#     print(100)
# else:
#     print(200)