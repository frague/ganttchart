#!/usr/bin/python

import datetime
from logging import getLogger

LOGGER = getLogger()

def parse_date(text):
    log = "Date \"%s\" parsing: " % text
    if isinstance(text, datetime.date):
    	return text

    try:
        d = datetime.datetime.strptime(str(text).strip(), "%m/%d/%Y").date()
    except:
        LOGGER.error("%s FAILED" % log)
        return None
    w = d.weekday()
    if w in (5, 6):
        d -= datetime.timedelta(days=w-4)
    LOGGER.debug("%s returned %s" % (log, d))
    return d

def printable_date(d):
    return d.strftime("%d/%m/%Y")
