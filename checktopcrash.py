import requests
import base64
import json
import simplejson
import urllib


bugList = []

class Bug:
	def __init__(self, iD):
		self.iD = iD
		self.sigList = []
		self.topCrash = []

url = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,cf_crash_signature,status&f1=cf_tracking_firefox39&f2=cf_crash_signature&o1=equals&o2=isnotempty&resolution=---&v1=%2B'
search_results=requests.get(url)
json_string = json.loads(search_results.text)

for i in json_string['bugs']:
	tempID = str(i['id'])
	tempBug = Bug(tempID)
	temp = str(i['cf_crash_signature'])
	if temp.count('[@') > 1:
		temps = temp.split('[@')
		for i in temps:
			i = i.translate(None, ']').lstrip()
			tempBug.sigList.append(i)
	elif temp.count('[@') == 1:
		temp = temp[2:]
		temp = temp.translate(None, ']').lstrip()
		tempBug.sigList.append(temp)

	bugList.append(tempBug)


url2 = 'https://crash-stats.mozilla.com/api/TCBS/?product=Firefox&version=39.0b&crash_type=Browser'
crash_results = requests.get(url2)
json_string2 = json.loads(crash_results.text)

for k in json_string2['crashes']:
	tempSig = str(k["signature"])
	#print tempSig
	for l in bugList:
		for x in l.sigList:
			if x == tempSig:
				l.topCrash.append(str(k["currentRank"] + 1))



for bugs in bugList:
	if len(bugs.topCrash) > 0:
		print "Bug " + bugs.iD + " has " + str(len(bugs.sigList)) + " crash signatures, and their ranks are: ",
		for crashes in bugs.topCrash:
			print crashes
