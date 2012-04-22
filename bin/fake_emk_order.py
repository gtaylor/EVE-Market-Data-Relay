#!/usr/bin/env python
"""
A fake order upload script, used to manually test the whole stack.
"""
import simplejson
import requests
import zlib

data = {
    'log': '2493384468,s,30005302,60010306,1599999.97,65,21.0,1,2012-04-04 09:50:43,90,32767\r\n2491011721,s,30005310,60010342,1600000.0,16,1.0,1,2012-04-02 03:43:36,90,32767\r\n2290291372,b,30005325,60011905,102000.0,200,197.0,1,2012-02-07 06:36:40,90,32767\r\n',
    'developer_key': 'EVEUnifiedUploader',
    'type_id': '12824',
    'upload_key': '45',
    'version': '6.0',
    'upload_type': 'orders',
    'generated_at': '2012-04-21 23:31:56',
    'region_id': '10000068',
}

data = {}

r = requests.post(
    #'http://master.eve-emdr.com/upload/unified/',
    'http://localhost:8080/upload/',
    data=data,
)
print "Sent fake order."
print r.status_code, r.text
