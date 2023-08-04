from __future__ import print_function

import os.path
from datetime import datetime, timedelta

import pandas as pd
import utils
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from pytz import all_timezones

PYGCAL_PATH = os.path.expanduser("~/.pygcal/")

# if modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

with open(PYGCAL_PATH + "timezone.txt") as file:
    TIMEZONE = file.readline()


def auth():
    """Authorize user. Get token if not there."""

    # need to move so all token/creds are in ~/.pygcal
    creds = None

    # token.json stores user's access and refresh tokens - create when authed
    if os.path.exists(PYGCAL_PATH + "token.json"):
        creds = Credentials.from_authorized_user_file(
            PYGCAL_PATH + "token.json", SCOPES
        )

    # if no (valid) creds - user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                PYGCAL_PATH + "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # save the credentials for the next run
        with open(PYGCAL_PATH + "token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def gcal_api_call(func):
    """Wrapper for calling calendar api."""

    def wrapper(*args, **kwargs):
        creds = auth()
        try:
            service = build("calendar", "v3", credentials=creds)
            func(service, *args, **kwargs)
        except HttpError as error:
            print("An error occurred: %s" % error)

    return wrapper


@gcal_api_call
def upcoming(service, num_events=10, verbose=False):
    """Get upcoming calendar entries."""
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time

    events_result = (
        service.events()
        .list(
            calendarId="primary",  # may be paramaterized
            timeMin=now,
            maxResults=num_events,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    utils.display_events(events, verbose=verbose)


@gcal_api_call
def add_event(service, start_time, end_time, summary, description=""):
    """Add an event to the calendar."""
    event = {
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": TIMEZONE,
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": TIMEZONE,
        },
        "summary": summary,
        "description": description,
    }

    event = service.events().insert(calendarId="primary", body=event).execute()
    print(f"Event created {event.get('htmlLink')}")


def set_timezone():
    """Set timezone for calendar."""
    timezone = input("Timezone: ").strip()
    with open(PYGCAL_PATH + "timezone.txt", "w") as file:
        file.write(timezone)


def init_csv():
    """Initialise csv with headers to add events."""
    headers = ["start_time", "summary", "description"]
    df = pd.DataFrame(columns=headers)
    df.to_csv(PYGCAL_PATH + "timers.csv", index=False)


def start_event(event_name, description=""):
    """Start recording an event."""
    if not os.path.exists(PYGCAL_PATH + "timers.csv"):
        init_csv()

    timers_df = pd.read_csv(PYGCAL_PATH + "timers.csv")

    if not event_name in timers_df["summary"].values:
        new_event = pd.DataFrame(
            [
                {
                    "start_time": datetime.now().isoformat(),
                    "summary": event_name,
                    "description": description,
                }
            ]
        )
        timers_df = pd.concat([timers_df, new_event], ignore_index=True)
        timers_df.to_csv(PYGCAL_PATH + "timers.csv", index=False)


def end_event(event_name):
    """Stop recording event and add to calendar."""
    if TIMEZONE not in all_timezones:
        print("Error: Timezone is not in the list of valid timezones.")
        return

    if not os.path.exists(PYGCAL_PATH + "timers.csv"):
        print("Error: Timers database not created, no running timers.")
        return

    timers_df = pd.read_csv(PYGCAL_PATH + "timers.csv")
    if len(timers_df["summary"].values) == 0:
        print("Error: No active timers.")
        return

    try:
        event_row = timers_df.loc[timers_df["summary"] == event_name].iloc[0]

        start_time = datetime.fromisoformat(event_row["start_time"])
        end_time = datetime.now()
        summary = event_row["summary"]
        description = event_row["description"]
        add_event(start_time, end_time, summary, description)
        timers_df = timers_df.drop(event_row.name)
        timers_df.to_csv(PYGCAL_PATH + "timers.csv", index=False)
    except IndexError:
        print(f"Error: No event with name {event_name} could be found.")
