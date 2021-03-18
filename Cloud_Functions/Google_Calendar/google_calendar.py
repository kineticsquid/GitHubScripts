"""
https://developers.google.com/calendar/quickstart/python

https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/index.html

calendar menu id = 'nfdcum6lvge3s6f3mnl78k25ro@group.calendar.google.com'


"""
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar'
MENU_CALENDAR_ID = 'nfdcum6lvge3s6f3mnl78k25ro@group.calendar.google.com'


def main(request_input):

    print("Input:")
    print(request_input)
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # events_result = service.events().list(calendarId=MENU_CALENDAR_ID, timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])
    # calendars = service.calendarList().list().execute()

    if request_input.get('action') == 'test':
        print("Testing...")
    thisday_ordinal = request_input.get('thisday', None)
    if thisday_ordinal is None:
        thisday_ordinal = datetime.datetime.now().toordinal()
    else:
        thisday_ordinal = int(thisday_ordinal)
    number_successful = 0
    print("Results:")
    for day in range(thisday_ordinal + 1, thisday_ordinal + 8):
        this_day = datetime.datetime.fromordinal(day).strftime("%Y-%m-%d")
        next_day = datetime.datetime.fromordinal(day+1).strftime("%Y-%m-%d")
        if day == thisday_ordinal + 7:
            new_event = {"start": {"date": this_day}, "end": {"date": next_day},
                         "description": "\n\nhttps://us-east.functions.appdomain.cloud/api/v1/web/" +
                                        "634e7a7f-9928-4744-8190-f4bf5d671142/utils/google-calendar?thisday=" + str(day),
                         "notes": day}
        else:
            new_event = {"start": {"date": this_day}, "end": {"date": next_day},
                         "notes": day}
        insert_result = service.events().insert(calendarId=MENU_CALENDAR_ID, body=new_event).execute()
        if insert_result.get('status') == 'confirmed':
            number_successful += 1
        print(insert_result)

    return_result = "Created %s calendar entries starting on %s" % \
                    (number_successful, datetime.datetime.fromordinal(thisday_ordinal+1).strftime("%Y-%m-%d"))
    print(return_result)
    return {"statusCode": 200, "body": return_result}


if __name__ == '__main__':
    today = datetime.datetime.now().toordinal()
    main({"action": "test",
          "thisday": 737035})
