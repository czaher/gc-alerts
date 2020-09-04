# gc_alerts
Pushes event notifications from a google calendar to ms teams or other webhooks-enabled chat applications.

  calendarJob.py will look for upcoming events every 5 minutes with a range of 15 minutes.
    If there is an upcoming event this script will draft a message in json and push that message to a webhooks connector specified in line 11.
  
  calendarDailySummary.py is written to run at 7am through cron and look for events that happen between that time and midnight of that day. 
    If there are any upcoming events that day this script will draft a message for each upcoming event and push that message to a webhooks connector specified in line 11. 
