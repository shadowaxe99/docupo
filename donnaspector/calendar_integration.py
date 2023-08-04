from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class CalendarIntegration:
    def __init__(self, creds):
        self.service = build('calendar', 'v3', credentials=creds)

    def schedule_event(self, event):
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        return event['id']