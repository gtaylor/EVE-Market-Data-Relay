#!/usr/bin/env python
"""
A fake history upload script, used to manually test the whole stack.
"""
import ujson
import requests
import zlib

data = """
{
  "resultType" : "history",
  "version" : "0.1alpha",
  "uploadKeys" : [
    { "name" : "emk", "key" : "abc" },
    { "name" : "ec" , "key" : "def" }
  ],
  "generator" : { "name" : "Yapeal", "version" : "11.335.1737" },
  "currentTime" : "2011-10-22T15:46:00+00:00",
  "columns" : ["date","orders","quantity","low","high","average"],
  "rowsets" : [
    {
      "generatedAt" : "2011-10-22T15:42:00+00:00",
      "regionID" : 10000065,
      "typeID" : 11134,
      "rows" : [
        ["2011-12-03T00:00:00+00:00",40,40,1999,499999.99,35223.50],
        ["2011-12-02T00:00:00+00:00",83,252,9999,11550,11550]
      ]
    }
  ]
}
"""

message = ujson.dumps(ujson.loads(data))

headers = {
    #'Content-Encoding': 'deflate'
}

# POST non-form encoded
data = message

# POST form-encoded
#data = {'data': message}

# Compressed request
#data = zlib.compress(data)#[2:-4]

r = requests.post(
    'http://localhost:8080/upload/unified/',
    data=data,
    headers=headers,
)

print "RESPONSE"
print r.text