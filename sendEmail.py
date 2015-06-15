#!/usr/bin/python

import smtplib
import os
import email
import email.encoders
import email.mime.text

sender = 'fakebugzilla@gmail.com'
receivers = 'katglazko@gmail.com'

message = """From: Your Friendly Crash Program <fakezilla@gmail.com>
To: Release Managers <katglazko@gmail.com>
Subject: Crashes for the week of 06/15

Bug ID  Crash Sig  #
zzzzz    !$$$S     279
"""

try:
	smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	smtpObj.starttls()
	smtpObj.login('fakebugzilla@gmail.com','Testtest1')
	smtpObj.sendmail(sender, receivers, message)      
	print "Successfully sent email"
except smtplib.SMTPException:
   print "Error: unable to send email"