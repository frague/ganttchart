#!/usr/bin/python

import datetime
from logging import getLogger

LOGGER = getLogger()

def de_weekend(d):
    w = d.weekday()
    if w in (5, 6):
        d -= datetime.timedelta(days=w-4)
    return d

def parse_date(text):
    log = "Date \"%s\" parsing: " % text
    if isinstance(text, datetime.date):
    	return de_weekend(text)

    try:
        d = datetime.datetime.strptime(str(text).strip(), "%d/%m/%Y").date()
    except:
        try:
            d = datetime.datetime.strptime(str(text).strip(), "%d.%m.%Y").date()
        except:
            LOGGER.error("%s FAILED" % log)
            return None
    LOGGER.debug("%s returned %s" % (log, d))
    return de_weekend(d)

def printable_date(d):
    return d.strftime("%d/%m/%Y")
