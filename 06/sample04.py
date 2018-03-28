import re

s = "hoge"
b = b"1234-hoge"

if re.match(r'^\d{4}-', b.decode('utf-8')):
    print(100)
else:
    print(200)