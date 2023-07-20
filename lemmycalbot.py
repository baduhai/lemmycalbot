#!/usr/bin/env python

import os
import sched
import argparse
from datetime import datetime
from pythorhead import Lemmy

CALE = os.getenv('CALENDAR')
INST = os.getenv('INSTANCE')
USER = os.getenv('USERNAME')
PASS = os.getenv('PASSWORD')
COMM = os.getenv('COMMUNITY')

s = sched.scheduler()
parser = argparse.ArgumentParser(
                    prog = 'LemmyCalBot',
                    description = 'Calendar based, post-scheduling, Lemmy bot.',
                    epilog = "Instead of arguments, environment variables may also be used, set CALENDAR, INTANCE, USERNAME, PASSWORD and COMMUNITY. Environment variables take precedence over arguments.")

parser.add_argument('-c', '--calendar', nargs = 1, help = 'Calendar address, beginning with webcal://')
parser.add_argument('-i', '--instance', nargs = 1, help = 'Instance address, e.g. https://sopuli.xyz')
parser.add_argument('-u', '--username', nargs = 1, help = 'Bot account username')
parser.add_argument('-p', '--password', nargs = 1, help = 'Bot account password')
parser.add_argument('-!', '--community', nargs = 1, help = 'Community name, e.g. indycar')
args = parser.parse_args()

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

def lemmyInit():
    lemmy = Lemmy(INST)
    lemmy.log_in(USER, PASS)
    community_id = lemmy.discover_community(COMM)

def createSessionThread(title, body=""):
    url = title.lower().replace(" ", "_")
    lemmy.post.create(community_id, title, url, body)

