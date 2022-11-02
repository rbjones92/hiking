# Robert Jones
# 10.4.22
# google calendar API connection

import datetime
import os.path
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

NOW = datetime.datetime.utcnow().isoformat() + "Z"
CLIENT_SECRET_FILE = 'client_secret.json'
API_KEY = 'AIzaSyAxI7kq-LdGR1QIWqV9LrrfKEzM95DUybc'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']
ALL_EVENTS = []
HIKE_CAL_ID = 'd25c55c05b60c9c15f1d15d21be8a6d84342aa525c1f348ad7c0969448fadef1@group.calendar.google.com'

def connect():

    ### Establish credentials and grab token #### 
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
    if not creds or not creds.valid:
        # Causes an error...
        '''
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
        '''
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE,SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json','w') as token:
            token.write(creds.to_json())

    service = build('calendar','v3',credentials=creds)

    return service


def create_events(service):
    import sqlite3
    import re
    loc_list = []
    distance_list = []
    date_list = []

    # Connect to hikes.db
    sqliteConn = sqlite3.connect('hikes.db')
    cursor = sqliteConn.cursor()
    cursor.execute('SELECT location FROM hikes')
    records = cursor.fetchall()

    for i in records:
        i = str(i).replace(',','')
        loc_list.append(i)

    cursor.execute('SELECT date FROM hikes')
    records = cursor.fetchall()

    for i in records:
        i = str(i).replace(',','')
        date_list.append(i)

    cursor.execute('SELECT distance FROM hikes')
    records = cursor.fetchall()

    for i in records:
        i = str(i).replace(',','')
        distance_list.append(i)        

    for j in range(len(date_list)):
        date_list[j] = datetime.datetime(int(date_list[j][8:12]),int(date_list[j][2:4]),int(date_list[j][5:7]),int('09')).isoformat()

    pattern = '\W'
    pattern2 = '[)(,]'
    for i in range(len(date_list)):

        event_request_body = {
            'start' : {
                'dateTime': date_list[i],
                'timeZone': 'PST'
            },
            'end': {
                'dateTime': date_list[i],
                'timeZone': 'PST'
            },
            'summary': f"Hiking at {re.sub(pattern,' ',loc_list[i])}",
            'description': f"{re.sub(pattern2,'',distance_list[i])} mile hike",
            'colorId': 5,
            'status': 'confirmed',
            'visibility':'public',
            'location':f"Hiking at {re.sub(pattern,' ',loc_list[i])}"
        }

        service.events().insert(calendarId = HIKE_CAL_ID,body = event_request_body).execute()


def list_events(service):
    ### LIST EVENTS### 
    while True:
        page_token = None
        events = service.events().list(calendarId=HIKE_CAL_ID, pageToken=page_token).execute()
        for event in events['items']:
            print(event['summary'])
        page_token = events.get('nextPageToken')
        if not page_token:
            break


def delete_events(service):
    ### DELETE ALL EVENTS### 
    while True:
        page_token = None
        events = service.events().list(calendarId=HIKE_CAL_ID, pageToken=page_token).execute()
        for event in events['items']:
            service.events().delete(calendarId=HIKE_CAL_ID, eventId=event['id']).execute()
        page_token = events.get('nextPageToken')
        if not page_token:
            break


### CREATE HIKES ###
delete_events(connect())
create_events(connect())