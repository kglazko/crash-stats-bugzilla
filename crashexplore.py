import requests
import base64
import json
import simplejson
import urllib



r = requests.get('https://bugzilla.mozilla.org/rest/login?login=fakebugzilla@gmail.com&password=Testtest1')
#print r.text

#Making a list to hold strings of crash signatures, it's empty right now.
crash_sigs = []
url_list = []

#specify which fields I want to send to the bugzilla API
url = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,cf_crash_signature,status&f1=cf_tracking_firefox39&f2=cf_crash_signature&o1=equals&o2=isnotempty&resolution=---&v1=%2B'

#I'm grabbing the URL and turning it into a JSON string, which I will parse in the next call.
search_results=requests.get(url)
json_string = json.loads(search_results.text)

#I'm parsing the JSON string and grabbing the crash signatures from the bugs, and I'm stripping out unneeded spaces and symbols.
#Also populating the list that I made earlier.
for i in json_string['bugs']:
	temp = str(i['cf_crash_signature'])
	if temp.count('[@') > 1:
		temps = temp.split('[@')
		for i in temps:
			i = i.translate(None, ']').lstrip()
			crash_sigs.append(i)
	elif temp.count('[@') == 1:
		temp = temp.translate(None, '[@]').lstrip()
		crash_sigs.append(temp)

print str(len(crash_sigs)) + " signatures in the list."

#This is where I convert my crash sigs into 'url friendly' format
for j in crash_sigs:
	temp = urllib.quote_plus(j)
	url_list.append(temp)


	#.translate(None, '[@]').lstrip()

#Going through the crash_sigs strings, sending them to the crash-stats API, and returning a JSON object of their crash frequencies. And it doesn't work!
for i in url_list:
	r = requests.get('https://crash-stats.mozilla.com/api/CrashesFrequency/?signature=' + i)
	print i
	print r.json()
