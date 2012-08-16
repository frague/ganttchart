#!/usr/bin/python

import datetime

def parse_date(text):
    try:
        d = datetime.datetime.strptime(str(text).strip(), "%m/%d/%Y").date()
    except:
        return None
    w = d.weekday()
    if w in (5, 6):
        d -= datetime.timedelta(days=w-4)
    return d

def printable_date(d):
    return d.strftime("%d/%m/%Y")
