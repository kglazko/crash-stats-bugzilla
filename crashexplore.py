import requests
import base64
import json
import simplejson

r = requests.get('https://bugzilla.mozilla.org/rest/login?login=kglazko@mozilla.com&password=Jimdog90')
#print r.text

crash_sigs = []
##specify which fields I want 
#u = url + "?token=507775-VtnSTxLefh&f1=cf_tracking_firefox39&o1=equals&v1=%2B&include_fields=id"
url = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,cf_crash_signature,status&f1=cf_tracking_firefox39&f2=cf_crash_signature&o1=equals&o2=isnotempty&resolution=---&v1=%2B'
search_results=requests.get(url)
#print search_results.text
json_string = json.loads(search_results.text)

for i in json_string['bugs']:
	#print (str(i['cf_crash_signature']).translate(None, ']@['))
	crash_sigs.append(str(i['cf_crash_signature']).translate(None, ']@[').lstrip())

for i in crash_sigs:
	r = requests.get('https://crash-stats.mozilla.com/api/CrashesFrequency/?signature=' + i)
	print i
	print r.json()

#j = json.loads(search_results)
#json_string = json.dumps(j,sort_keys=True,indent=2)
#print json_string
#for key,value in search_results.iteritems():
	#print key, value
	#print len(value)

#json_raw = json.loads(search_results)
