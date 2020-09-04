'''
Open google calendar API page with event range of [current time - time in 15 mins]
'''

import datetime
import requests
import json
import os
#import webbrowser

webhook_url = ''

#set current time (7 AM)
now = datetime.datetime.now()

#format for RFC3339
nowTime = now.strftime("%H:%M:00")
nowDate = now.strftime("%Y-%m-%d")
timeMin = (nowDate+"T"+nowTime+"-04:00")
#print("timeMin: " + timeMin)

#set time, 17 hours from now (Midnight)
later = datetime.datetime.now() + datetime.timedelta(hours=17)

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

itemCount = 0

#iterate through all items, pull item summaries and descriptions
for event in jsonresp['items']:
    startTimeStr = event["start"]["dateTime"]
    startTimeObj = datetime.datetime.strptime(startTimeStr, '%Y-%m-%dT%X-04:00')
    startTimeSend = datetime.datetime.strftime(startTimeObj, '%-I:%M %p')
    itemCount = itemCount + 1
    
#prepare and send Teams message with event info
        
    if itemCount > 0:
        teams_data = {'text': "Event today: " + " \"" + event["summary"] + "\" " + " Starts at: " + startTimeSend + " Description: \"" + event["description"] +"\"" }

        response = requests.post( webhook_url, data=json.dumps(teams_data), headers={'Content-Type': 'application/json'})
        
if itemCount == 0:
    teams_data = {'text': "There are no events today." }
    response = requests.post( webhook_url, data=json.dumps(teams_data), headers={'Content-Type': 'application/json'})

#close confirmation
print() 
input('press ENTER to exit')
