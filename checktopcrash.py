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
		self.topCrash.append([])
		self.topCrash.append([])


file_object = open("39_crashrank.text", "wb")
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
				l.topCrash[0].append(str(k["currentRank"] + 1))
				l.topCrash[1].append("39.0b")

url3 = 'https://crash-stats.mozilla.com/api/TCBS/?product=Firefox&version=39.0b1&crash_type=Browser'
crash_results3 = requests.get(url3)
json_string3 = json.loads(crash_results3.text)

for k in json_string3['crashes']:
	tempSig = str(k["signature"])
	#print tempSig
	for l in bugList:
		for x in l.sigList:
			if x == tempSig:
				l.topCrash[0].append(str(k["currentRank"] + 1))
				l.topCrash[1].append("39.0b1")

url4 = 'https://crash-stats.mozilla.com/api/TCBS/?product=Firefox&version=39.0b2&crash_type=Browser'
crash_results4 = requests.get(url4)
json_string4 = json.loads(crash_results4.text)

for k in json_string4['crashes']:
	tempSig = str(k["signature"])
	#print tempSig
	for l in bugList:
		for x in l.sigList:
			if x == tempSig:
				l.topCrash[0].append(str(k["currentRank"] + 1))
				l.topCrash[1].append("39.0b2")

url5 = 'https://crash-stats.mozilla.com/api/TCBS/?product=Firefox&version=39.0b3&crash_type=Browser'
crash_results5 = requests.get(url5)
json_string5 = json.loads(crash_results5.text)

for k in json_string5['crashes']:
	tempSig = str(k["signature"])
	#print tempSig
	for l in bugList:
		for x in l.sigList:
			if x == tempSig:
				l.topCrash[0].append(str(k["currentRank"] + 1))
				l.topCrash[1].append("39.0b3")

url6 = 'https://crash-stats.mozilla.com/api/TCBS/?product=Firefox&version=39.0b4&crash_type=Browser'
crash_results6 = requests.get(url6)
json_string6 = json.loads(crash_results6.text)

for k in json_string6['crashes']:
	tempSig = str(k["signature"])
	#print tempSig
	for l in bugList:
		for x in l.sigList:
			if x == tempSig:
				l.topCrash[0].append(str(k["currentRank"] + 1))
				l.topCrash[1].append("39.0b4")



for bugs in bugList:
	if len(bugs.topCrash[0]) > 0:
		print "Bug " + bugs.iD + " has a crash ranked: " 
		file_object.write("Bug " + bugs.iD + " has a crash ranked:\n")
		count = len(bugs.topCrash[0])
		for l in range(0, count):
			print (bugs.topCrash[0][l]),
			file_object.write(bugs.topCrash[0][l]),
			print " in: " + (bugs.topCrash[1][l])
			file_object.write(" in: " + (bugs.topCrash[1][l]) + "\n")

file_object.close()
			
