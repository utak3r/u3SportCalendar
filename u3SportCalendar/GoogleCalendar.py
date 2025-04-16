import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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

    def get_events(self, calendarId, timeStart, timeEnd):
        # https://developers.google.com/workspace/calendar/api/v3/reference/events/list?hl=pl
        # timeMin, timeMax - Musi być sygnaturą czasową w formacie RFC3339 
        # z obowiązkowym przesunięciem strefy czasowej, np. 
        # 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z. 
        # Można podać milisekundy, ale zostaną one zignorowane.
        # singleEvents - czy rozwijać wydarzenia cykliczne do pojedynczych wystąpień.

        events = None
        if (self.creds is not None):
            if (self.api_service_resource is not None):
                timeMin = timeStart.isoformat(timespec='seconds')
                timeMax = timeEnd.isoformat(timespec='seconds')
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
                    events = events_result.get("items", [])
                except HttpError as error:
                    print(f"An error occurred: {error}")
            else:
                print("API service not build.")
        else:
            print("Not authorized.")
        
        return events
    
