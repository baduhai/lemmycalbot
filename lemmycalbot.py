#!/usr/bin/env python

import os
import time
import pytz
import sched
import requests
import argparse
from dateutil import parser
from pythorhead import Lemmy
from icalendar import Calendar
from tzlocal import get_localzone
from datetime import datetime, timezone

parser = argparse.ArgumentParser(
    prog = 'lemmycalbot',
    description = 'Calendar based, post-scheduling, Lemmy bot.',
    epilog = "Instead of arguments, environment variables may also be used, set CALENDAR, INSTANCE, USERNAME, PASSWORD and COMMUNITY. Environment variables take precedence over arguments.")
parser.add_argument('-c', '--calendar', nargs = 1, help = 'Calendar address, make sure to replace webcal:// with https:// or http://')
parser.add_argument('-i', '--instance', nargs = 1, help = 'Instance address, e.g. https://sopuli.xyz')
parser.add_argument('-u', '--username', nargs = 1, help = 'Bot account username')
parser.add_argument('-p', '--password', nargs = 1, help = 'Bot account password')
parser.add_argument('-!', '--community', nargs = 1, help = 'Community name, e.g. indycar')
args = parser.parse_args()

CALE = os.getenv('CALENDAR')
INST = os.getenv('INSTANCE')
USER = os.getenv('USERNAME')
PASS = os.getenv('PASSWORD')
COMM = os.getenv('COMMUNITY')
if CALE is None:
    CALE = args.calendar[0]
    if CALE is None:
        exit("Calendar address not set")
if INST is None:
    INST = args.instance[0]
    if INST is None:
        exit("Instance address not set")
if USER is None:
    USER = args.username[0]
    if USER is None:
        exit("Bot account username not set")
if PASS is None:
    PASS = args.password[0]
    if PASS is None:
        exit("Bot account password not set")
if COMM is None:
    COMM = args.community[0]
    if COMM is None:
        exit("Community name not set")


s = sched.scheduler(time.time, time.sleep)

# Create post, still need to find out to pin post
def createSessionThread(title, body=""):
    lemmy = Lemmy(INST)
    lemmy.log_in(USER, PASS)
    community_id = lemmy.discover_community(COMM)
    url = title.lower().replace(" ", "_")
    print("Posting ", title)
    lemmy.post.create(community_id, title, body=body)

# Fetch calendar, and parse into raw ical
def fetchAndParseCalendar(url):
    response = requests.get(url)
    try:
        response.raise_for_status()
        calendar_data = response.text
        calendar = Calendar.from_ical(calendar_data)
        return calendar
    except requests.exceptions.HTTPError as e:
        print(f"An error occured while fetching the calendar: {e}")
        exit()

# Find closest upcoming event and schedule a post
def scheduleEvent(calendar, scheduler):
    now = datetime.now(get_localzone())
    upcoming_events = [
        (event.get('dtstart').dt, event.get('dtstart').params.get('TZID'), event) for event in calendar.walk('VEVENT') if event.get('dtstart').dt > now
    ]
    if upcoming_events:
        # Sort the events based on start time and get the closest upcoming event
        next_event_time, event_timezone, next_event = min(upcoming_events, key=lambda x: x[0])
        title = next_event.get('summary')
        body = next_event.get('description')
        # Check if the event_timezone is None, if so, use the computer's local timezone
        if event_timezone is None:
            event_tz = get_localzone()
        else:
            event_tz = pytz.timezone(event_timezone)
        # Convert the start time to the event's timezone
        next_event_time = next_event_time.astimezone(event_tz)
        # Convert the start time to a timestamp for the scheduler
        timestamp = time.mktime(next_event_time.timetuple())
        # Schedule the function for the closest upcoming event
        print("Next thread:", "\n", title, "\n", next_event_time, "\n", timestamp)
        s.enterabs(timestamp, 1, createSessionThread, (title, body))
    else:
        exit("No upcoming events found in the calendar.")


# Run main logic in while True loop to repeat program for as long as there are calendar events.
while True:
    cal = fetchAndParseCalendar(CALE)
    scheduleEvent(cal, s)
    s.run()

