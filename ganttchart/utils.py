#!/usr/bin/python

import datetime

def parse_date(text):
    try:
        return datetime.datetime.strptime(str(text), "%m/%d/%Y")
    except:
        return None

