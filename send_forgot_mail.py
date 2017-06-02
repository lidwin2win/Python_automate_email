#!/bin/python3.5
#python program to send email via gmail using SMTP protocol

import smtplib
import getpass
import sys
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from html.parser import HTMLParser

from bs4 import BeautifulSoup


def send_forgot_mail(email_id,pwd,toid,html_part):

	#1.create an object for smtp using the smtp of email server and port

	smtp_object = smtplib.SMTP('smtp.gmail.com',587)

	#2.using this object we should call ehlo though i do not understand the use of ehlo() then we start ttls which i believe is for security

	smtp_object.ehlo()

	smtp_object.starttls()

	smtp_object.login(email_id,pwd)

	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Forgot Password?'
	msg['From'] = email_id
	msg['To'] = toid

	recepient = msg['To']

	#text = str(input("Enter the text part of email:"))
	'''
	with open('template.html', 'r') as myfile:
    		html=myfile.read().replace('\n', '')
'''
	html = html_part

		
	#part1 = MIMEText(text, 'plain')
	part2 = MIMEText(html, 'html')


	#msg.attach(part1)
	msg.attach(part2)

	smtp_object.sendmail(email_id,recepient, msg.as_string())
	smtp_object.quit()



def dynamic_add(name,link,html_data):

	soup = BeautifulSoup(html_data,"html.parser")

	tag = soup.find('td',{'class':'headline'})

	tag.string='Hello '+name+' !'

	#print(tag)

	atag = soup.find('a')

	atag['href']=link	

	tag2 = soup.find('html')

	#print(tag2)

	return tag2

	

	

if __name__ == "__main__":


	toid = str(sys.argv[1])

	name = str(sys.argv[2])

	link = str(sys.argv[3])

	
	

	#3.now we login to our email account using login function
	#this worked only after i allowed less secure apps to access

	data = open('email_details.json','r')

	data= json.load(data)

	fromid = str(data['emailid'])

	pwd = str(data['pwd'])


	html_data = open('template.html','r+')	

	#print(html_data.read())

	html =	dynamic_add(name,link,html_data)

	#4.now we can send email to any valid gmail account !

	send_forgot_mail(fromid,pwd,toid,html)

	



