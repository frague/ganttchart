#!/usr/bin/python

from datetime import datetime
from exceptions import *
import Image, ImageDraw
from logging import getLogger
from utils import *

LOGGER = getLogger()

class Task:
    """ Represents task """
    def __init__(self, title, category, pool, owner, from_date=None, till_date=None, depends_on=None, length=None):
        self.title = title
        self.owner = owner
        self.pool = pool
        self.category = category

        self.from_date = parse_date(from_date)
        self.till_date = parse_date(till_date)

        if from_date and till_date:
            if not self.from_date or not self.till_date or not self.from_date <= self.till_date:
                LOGGER.error("Dates error: from_date=%s, till_date=%s" % (from_date, till_date))
                raise DatesError("Dates error: from_date=%s, till_date=%s" % (from_date, till_date))

        if depends_on and isinstance(depends_on, Task):
            self.depends_on = depends_on

        LOGGER.debug("Task created \"%s\"" % self)

    @property
    def key(self):
        try:
            return self.pool + self.owner + self.from_date.strftime("%Y%m%d")
        except Exception:
            return ""

    def __lt__(self, other):
        return self.key < other.key


    def __repr__(self):
        return "Task: \"%s\" (%s) [%s-%s]" % (self.title, self.owner, 
                printable_date(self.from_date), printable_date(self.till_date))

    def to_csv(self):
        return "%s,	%s,	%s,	%s,	%s" % (self.category.smart_title, self.pool, self.owner, 
                printable_date(self.from_date), printable_date(self.till_date))
