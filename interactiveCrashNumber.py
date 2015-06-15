import requests
import base64
import json
import simplejson
import urllib
import csv
import sys
import datetime
import smtplib
import os
import email
import email.encoders
import email.mime.text
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText


days = sys.argv[1]

version = str(sys.argv[2])

daysList = []

sendEmail = str(sys.argv[3])

print days
today = datetime.date.today()
print today
one_day = datetime.timedelta(days=1)

for i in range (0,int(days)):
	day = today - one_day * i
	daysList.append(day)

end_date = daysList[0] + one_day
start_date = daysList[len(daysList) -1]
 
#CSV Code Set-Up
#CSV CODE
f = open('crashesInRange.csv', 'wt')


bugList = []

class Bug:
	def __init__(self, iD):
		self.iD = iD
		self.sigs = []

class Sig:
	def __init__(self, iD):
		self.iD = iD
		self.crashWeek = 0

#r = requests.get('https://bugzilla.mozilla.org/rest/login?login=fakebugzilla@gmail.com&password=Testtest1')
#print r.text

#Making a list to hold strings of crash signatures, it's empty right now.
crash_sigs = []
url_list = []
url_list.append([])
url_list.append([])

#specify which fields I want to send to the bugzilla API
url = 'https://bugzilla.mozilla.org/rest/bug?include_fields=id,cf_crash_signature,status&f1=cf_tracking_firefox' + version + '&f2=cf_crash_signature&o1=equals&o2=isnotempty&resolution=---&v1=%2B'

#I'm grabbing the URL and turning it into a JSON string, which I will parse in the next call.
search_results=requests.get(url)
json_string = json.loads(search_results.text)

#I'm parsing the JSON string and grabbing the crash signatures from the bugs, and I'm stripping out unneeded spaces and symbols.
#Also populating the list that I made earlier.
for i in json_string['bugs']:
	tempID = str(i['id'])
	tempBug = Bug(tempID)
	temp = str(i['cf_crash_signature'])

	if temp.count('[@') > 1:
		temps = temp.split('[@')
		for i in temps:
			i = i.translate(None, ']').lstrip().rstrip()
			i = i.translate(None, '\n')
			tempSig = Sig(i)
			tempBug.sigs.append(tempSig)
	elif temp.count('[@') == 1:
		temp = temp[2:]
		temp = temp.translate(None, ']').lstrip().rstrip()
		tempSig = Sig(temp)
		tempBug.sigs.append(tempSig)
	bugList.append(tempBug)



#This is where I convert my crash sigs into 'url friendly' format
for b in bugList:
	for s in b.sigs:
		t = urllib.quote_plus(str(s.iD))
		url_list[0].append(t)
		url_list[1].append(str(s.iD))


	#.translate(None, '[@]').lstrip()

#Going through the crash_sigs strings, sending them to the crash-stats API, and returning a JSON object of their crash frequencies. And it doesn't work!
for i in range (0, len(url_list[0])):
		r = requests.get('https://crash-stats.mozilla.com/api/CrashesCountByDay/?signature='+ (url_list[0][i]) + '&start_date=' + str(daysList[len(daysList) -1]) + '&end_date=' + str(end_date))
		jsonStr = json.loads(r.text)
		if 'errors' not in jsonStr.keys():
			for b in bugList:
				for c in b.sigs:
					if url_list[1][i] == c.iD:
						for d in daysList:
							c.crashWeek = c.crashWeek + jsonStr['hits'][str(d)]
						


#for b in bugList:
	#for c in b.sigs:
		#print c.iD + " has had " + str(c.crashWeek) + " crashes last week."
			

writer = csv.writer(f)
writer.writerow(('Bug Id', 'Crash Signature', '# of Crashes'))
for bugs in bugList:
	for m in range (1, len(bugs.sigs)):
		writer.writerow( (bugs.iD,bugs.sigs[m].iD, bugs.sigs[m].crashWeek) )

f.close()





##### EMAIL SECTION ONLY #####
if sendEmail == 'y':
	sender = 'fakebugzilla@gmail.com'
	receivers = 'kglazko@mozilla.com'
	subject = 'Crashes for Dates ' + str(start_date) + " to " + str(today)
	message = "Version " + version + '\n'+ "Bug I.D.      # of Crashes\n"
	for b in bugList:
		temp = 0
		for c in b.sigs:
			temp = temp + c.crashWeek
		message = message + (str(b.iD)) + '      ' + (str(c.crashWeek)) + '\n'
	msg = email.MIMEMultipart.MIMEMultipart()
	msg['From'] = sender
	msg['To'] = receivers
	msg['Date'] = email.Utils.formatdate(localtime=True)
	msg['Subject'] = subject
	msg.attach(email.MIMEText.MIMEText(message))
	try:
		smtpObj = smtplib.SMTP('smtp.gmail.com:587')
		smtpObj.ehlo()
		smtpObj.starttls()
		smtpObj.login('fakebugzilla@gmail.com','Testtest1')
		smtpObj.sendmail(sender, receivers, msg.as_string())      
		print "Successfully sent email"
	except smtplib.SMTPException:
   		print "Error: unable to send email"
