#!/usr/bin/python3
'''
Module for Hodor level 0 challenge.

Has to add the 'id' and 'holdthedoor' fields to a proper POST request.

'''
import requests

url = 'http://158.69.76.135/level0.php'
data = {'id': '650', 'holdthedoor': 'Submit'}
success = 'Hold the Door challenge - Level 0'
votes = 1024
ok = 0
fail = 0

print("Starting {} votes:".format(votes))

while ok < votes and fail < 100:
    try:
        response = requests.post(url, data=data)
        if response.status_code is 200 and success in response.text:
            fail = 0
            ok += 1
            print("{} ok!".format(ok))
    except Exception as e:
        print(e)
        fail += 1

print("Finished: {}/{} votes.".format(ok, votes))
