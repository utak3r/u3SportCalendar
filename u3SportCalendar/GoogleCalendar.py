import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from u3SportCalendar.Events import Event, EventsList

class GoogleCalendar:

    def __init__(self):
        self.creds = None
        self.scopes = [
            "https://www.googleapis.com/auth/calendar.readonly",
            "https://www.googleapis.com/auth/calendar.events"
            ]
        self.api_service_resource = None

    def authorize(self):
        if (self.creds is None):
            if os.path.exists("token.json"):
                self.creds = Credentials.from_authorized_user_file("token.json", self.scopes)
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.scopes)
                    self.creds = flow.run_local_server(port=0)
                with open("token.json", "w") as token:
                    token.write(self.creds.to_json())

    def build_service(self):
        if (self.creds is not None):
            try:
                self.api_service_resource = build("calendar", "v3", credentials=self.creds)
            except HttpError as error:
                print(f"An error occurred: {error}")
        else:
            print("Not authorized.")

    def get_events(self, calendarId, timeStart:datetime.datetime, timeEnd:datetime.datetime):
        # https://developers.google.com/workspace/calendar/api/v3/reference/events/list?hl=pl
        # timeMin, timeMax - Musi być sygnaturą czasową w formacie RFC3339 
        # z obowiązkowym przesunięciem strefy czasowej, np. 
        # 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z. 
        # Można podać milisekundy, ale zostaną one zignorowane.
        # singleEvents - czy rozwijać wydarzenia cykliczne do pojedynczych wystąpień.

        events = EventsList()
        if (self.creds is not None):
            if (self.api_service_resource is not None):
                timeMin = Event.datetime_as_iso(timeStart)
                timeMax = Event.datetime_as_iso(timeEnd)
                try:
                    events_result = (
                        self.api_service_resource.events()
                        .list(
                            calendarId=calendarId,
                            timeMin=timeMin,
                            timeMax=timeMax,
                            singleEvents=True,
                            orderBy="startTime",
                        )
                        .execute()
                    )
                    events_api = events_result.get("items", [])
                    print(events_api)
                    for event in events_api:
                        summary = event["summary"]
                        start = datetime.datetime.fromisoformat(event["start"].get("dateTime", event["start"].get("date")))
                        end = datetime.datetime.fromisoformat(event["end"].get("dateTime", event["end"].get("date")))
                        local_tz = datetime.datetime.now().astimezone().tzinfo
                        start = start.astimezone(local_tz)
                        end = end.astimezone(local_tz)
                        events.add_event(Event(summary, start, end))
                        #print(f"{summary}: {start} - {end}")

                except HttpError as error:
                    print(f"An error occurred: {error}")
            else:
                print("API service not build.")
        else:
            print("Not authorized.")
        
        return events
    
    def insert_event(self, calendarId, event:Event):
        # TODO:
        # Use time zone from Event class (once it's working properly...)
        # see comment in Event.get_timezone_info()
        html_link = ""
        if (self.creds is not None):
            if (self.api_service_resource is not None):
                try:
                    event_api = {
                        'summary': event.name(),
                        'start': {
                            'dateTime': event.start().isoformat(timespec='seconds'),
                            'timeZone': 'Europe/Warsaw'
                        },
                        'end': {
                            'dateTime': event.end().isoformat(timespec='seconds'),
                            'timeZone': 'Europe/Warsaw'
                        }
                    }
                    event_result = (
                        self.api_service_resource.events()
                            .insert(calendarId=calendarId, body=event_api).execute()
                        )
                    html_link = event_result.get('htmlLink')
                except HttpError as error:
                    print(f"An error occurred: {error}")
        
        return html_link
    
