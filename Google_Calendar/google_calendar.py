"""
https://developers.google.com/calendar/quickstart/python

https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/index.html

calendar menu id = 'nfdcum6lvge3s6f3mnl78k25ro@group.calendar.google.com'


"""
import datetime
from googleapiclient.discovery import build
from oauth2client import file, client, tools
from flask import Flask, request, jsonify
import os
import json

PORT = os.getenv('PORT', '5040')
# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'
MENU_CALENDAR_ID = 'nfdcum6lvge3s6f3mnl78k25ro@group.calendar.google.com'
CALENDAR_SERVICE_URL = 'https://calendar.johnkellerman.org'

app = Flask(__name__)


@app.route('/')
def index():
    args = dict(request.args)

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    calendar_service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # events_result = service.events().list(calendarId=MENU_CALENDAR_ID, timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    # calendars = service.calendarList().list().execute()

    if args.get('test', None) != None:
        testing_results = []
        testing = True
        print("Testing...")
    else:
        testing = False
    thisday_ordinal = args.get('thisday', None)
    if thisday_ordinal is None:
        thisday_ordinal = datetime.datetime.now().toordinal()
    else:
        thisday_ordinal = int(thisday_ordinal)
    number_successful = 0
    print("Results:")
    for day in range(thisday_ordinal + 1, thisday_ordinal + 8):
        this_day = datetime.datetime.fromordinal(day).strftime("%Y-%m-%d")
        next_day = datetime.datetime.fromordinal(day + 1).strftime("%Y-%m-%d")
        if day == thisday_ordinal + 7:
            new_event = {"start": {"date": this_day}, "end": {"date": next_day},
                         "description": "\n\n<a href=\"%s?thisday=%s\">Create next week\'s entries</a>" % (CALENDAR_SERVICE_URL, str(day)),
                         "notes": day}
        else:
            new_event = {"start": {"date": this_day}, "end": {"date": next_day},
                         "notes": day}
        if not testing:
            insert_result = calendar_service.events().insert(calendarId=MENU_CALENDAR_ID, body=new_event).execute()
            if insert_result.get('status') == 'confirmed':
                number_successful += 1
            print(insert_result)
        else:
            testing_results.append(new_event)
    if not testing:
        return_result = "Created %s calendar entries starting on %s" % \
                    (number_successful, datetime.datetime.fromordinal(thisday_ordinal + 1).strftime("%Y-%m-%d"))
        print(return_result)
        return return_result
    else:
        print(json.dumps(testing_results))
        return jsonify(testing_results)


@app.route('/build')
def this_build():
    return app.send_static_file('build.txt')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(PORT))
