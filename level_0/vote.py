#!/usr/bin/python3
'''Module for Hodor level 0 challenge.'''
import requests

url = 'http://158.69.76.135/level0.php'
data = {'id': '650', 'holdthedoor': 'Submit'}
votes = 3
ok = 0

for i in range(votes):
    response = requests.post(url, data=data)
    if response.status_code is 200:
        ok += 1

print("Done! {}/{} votes submitted.".format(ok, votes))
