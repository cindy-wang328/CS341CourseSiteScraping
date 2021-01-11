#!/usr/bin/env python3
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime, timedelta
import random
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

REMINDER_MINUTES = 420 # Number of minutes BEFORE the event (420 means 5pm the day before the due date) since google doesn't let you put reminders after the fullday event already started


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    #If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    color = random.randint(1, 11)
    soup = BeautifulSoup(requests.get("https://student.cs.uwaterloo.ca/~cs341/").text, "html.parser")

    l = (soup.find(id="Lectures"))
    res = []
    tmp = {}
    tmp_description = []
    #a = soup.find(id="Assignments")
    for tr in l.find_all("tr"):
        tds = tr.find_all("td")
        if(tds and not tds[2].text == "February 15-19"): # >:((((( REEEEEEEE

            for x in tds:
                a = x.find_all("a")
                for link in a:
                    tmp_description.append(link.text)
                    tmp_description.append(link["href"])
                if len(a) == 0 and len(x.text) > 0:
                    tmp_description.append(x.text)



            if(len(tds) == 7): # Push the prev one 
                if tmp:
                    tmp["description"] = "\n".join(tmp_description)
                    res.append(tmp)
                    tmp = {}
                    tmp_description = []

                dt = (datetime.strptime(tds[2].text + " 2021", "%B %d %Y" ).strftime("%Y-%m-%d"))
                dt1 = (datetime.strptime(tds[2].text + " 2021", "%B %d %Y" ) + timedelta(days=1)).strftime("%Y-%m-%d")
                tmp["start"] = {"date": dt}
                tmp["end"] = {"date": dt1}
                tmp["summary"] = "CS341 " + tds[0].text

    if tmp: 
        tmp["description"] = "\n".join(tmp_description)
        res.append(tmp)
        tmp = {}
        tmp_description = []

    for e in res:
        e["colorId"] = str(color)
        e["reminders"] = {"useDefault": False, "overrides": [{"method": "popup", "minutes": REMINDER_MINUTES}]}
        event = service.events().insert(calendarId="primary", body=e).execute()
        print("event " + e["summary"] + " created")


    # Assignments
    color = random.randint(1, 11)
    a = soup.find(id="Assignments")
    a341 = []
    for tr in a.find_all("tr"):
        tds = tr.find_all("td")
        a341.append([x.text for x in tds])

    for l in a341:
        if len(l) > 0:
            dt = (datetime.strptime(l[2] + " 2021", "%A, %B %d %Y" ).strftime("%Y-%m-%d"))
            dt1 = (datetime.strptime(l[2] + " 2021", "%A, %B %d %Y" ) + timedelta(days=1)).strftime("%Y-%m-%d")
            evt = {
                  "summary": "CS341 " + str(l[0]),
                  "description": "CS341 Assignment",
                  "start": {
                    "date": dt,
                  },
                  "end": {
                    "date": dt1
                  },
                  "recurrence": [],
                  "attendees": [],
                  "reminders": {
                    "useDefault": False,
                    "overrides": [
                      {
                        "method": "popup",
                        "minutes": REMINDER_MINUTES
                      }
                    ]
                  },
                  "colorId": str(color)
                }
            event = service.events().insert(calendarId="primary", body=evt).execute()
            print("event " + evt["summary"] + " created")


if __name__ == '__main__':
    main()
