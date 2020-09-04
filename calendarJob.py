'''
Open google calendar API page with event range of [current time - time in 15 mins]
'''

import datetime
import requests
import json
import os
#import webbrowser

webhook_url = ''

#set current time
now = datetime.datetime.now()

#format for RFC3339
nowTime = now.strftime("%H:%M:00")
nowDate = now.strftime("%Y-%m-%d")
timeMin = (nowDate+"T"+nowTime+"-04:00")
#print("timeMin: " + timeMin)

#set time, 15 mins from now
later = datetime.datetime.now() + datetime.timedelta(minutes=16)

#format for RFC3339
laterTime = later.strftime("%H:%M:%S")
laterDate = later.strftime("%Y-%m-%d")
timeMax = (laterDate+"T"+laterTime+"-04:00")
#print("timeMax: " + timeMax)
print("timeMin",now)
print("timeMax",later)
#generate url
url = "https://www.googleapis.com/calendar/v3/calendars/...&timeMin=" + timeMin + "&timeMax=" + timeMax

#webbrowser.open(url)

response = requests.get(url)

jsonresp = json.loads(response.text)

#iterate through all items, pull item summaries and descriptions
for event in jsonresp['items']:
    startTimeStr = event["start"]["dateTime"]
    startTimeObj = datetime.datetime.strptime(startTimeStr, '%Y-%m-%dT%X-04:00')
    timeDiff = startTimeObj - datetime.datetime.now()
    startTimeSend = datetime.datetime.strftime(startTimeObj, '%-I:%M %p')
    timeTill = " "
    sendIt = 1
    
    if timeDiff < datetime.timedelta(minutes=1) and timeDiff > datetime.timedelta(minutes=-1):
        timeTill = "Event starting now: "
        print(event["summary"])
        sendIt = 1
        
    elif timeDiff < datetime.timedelta(minutes=6) and timeDiff > datetime.timedelta(minutes=1):
        timeTill = "Event starting in 5 minutes: "
        print(event["summary"])
        sendIt = 1
        
    elif timeDiff < datetime.timedelta(minutes=11) and timeDiff > datetime.timedelta(minutes=6):
        timeTill = "Event starting in 10 minutes: "
        print(event["summary"])
        sendIt = 1
        
    elif timeDiff < datetime.timedelta(minutes=16) and timeDiff > datetime.timedelta(minutes=11):
        timeTill = "Event starting in 15 minutes: "
        print(event["summary"])
        sendIt = 1
        
    elif timeDiff < datetime.timedelta(minutes=0):
        sendIt = 0
        
#prepare and send Teams message with event info
    if sendIt == 1:
        teams_data = {'text': timeTill + " \"" + event["summary"] + "\" " + " Starts at: " + startTimeSend + " Description: \"" + event["description"] +"\"" }
    
        response = requests.post( webhook_url, data=json.dumps(teams_data), headers={'Content-Type': 'application/json'})

#close confirmation
print() 
input('press ENTER to exit')
