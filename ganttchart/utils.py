#!/usr/bin/python

import datetime

def parse_date(text):
    try:
        return datetime.datetime.strptime(str(text), "%m/%d/%Y").date()
    except:
        return None

def printable_date(d):
    return d.strftime("%d/%m/%Y")
