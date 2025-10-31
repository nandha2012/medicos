#!/usr/bin/env python
import requests
data = {
    'token': 'E2CAE892A6D129154430EF07AE11EFE7',
    'content': 'log',
    'logtype': 'record',
    'user': '',
    'record': '',
    'beginTime': '2025-06-19 01:00',
    'endTime': '2025-06-20 00:21',
    'format': 'json',
    'returnFormat': 'json'
}
r = requests.post("end_point",data=data)
print('HTTP Status: ' + str(r.status_code))
print(r.json())
