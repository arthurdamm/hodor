#!/usr/bin/python3
'''
Module for Hodor level 3 challenge.

Has to have a WINDOW's user agent.

Has to use pytesseract to read a CAPTCHA image off the server.

Has to parse the hidden 'key' field's 'value' from a GET request

Has to add the user's 'id' and 'holdthedoor' fields to POST request.

'''
import requests
import re
import time
import pytesseract
from PIL import Image

url = 'http://158.69.76.135/level3.php'
captcha_url = 'http://158.69.76.135/captcha.php'
data = {'id': '650', 'holdthedoor': 'Submit'}
referer = url
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
headers = {'User-Agent': agent, 'Referer': url}
success = 'Hold the Door challenge - Level 3'
votes = 1024
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

        response = s.get(captcha_url, headers=headers)
        f = open('captcha.png', 'wb')
        f.write(response.content)
        f.close()
        data["captcha"] = \
            pytesseract.image_to_string(Image.open('captcha.png'))
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
