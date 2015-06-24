import requests
import base64
import json
import simplejson
import urllib
import httplib
import csv
import sys

#This will be where the code imports the bug ID and the comment to post
bug_id = 0
comment = ""

#Stuff for the POST request for comments
host = 'https://bugzilla.mozilla.org'
url = '/rest/bug/1088406/comment'
params = {'api_key':'SwkCr8vriP2tqxWvwub0m2KV6ODDxo7JjVyFr931', 'id': 1088406, 'comment': "This is a testing comment"}

#Actually submit the POST request and print the comment ID
r = requests.post((host+url), data = params)
iD = json.loads(r.text)
print iD.keys()
print iD['id']
