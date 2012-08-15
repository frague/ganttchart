#!/usr/bin/python

from datetime import datetime
from exceptions import *
import Image, ImageDraw

class Task:
    """ Represents task """
    def __init__(self, title, category, owner, from_date=None, till_date=None, depends_on=None, length=None):
        self.title = title
        self.owner = owner
        self.category = category
        if from_date and till_date:
            if not isinstance(from_date, datetime) or not isinstance(till_date, datetime)\
            or not from_date < till_date:
                raise DatesError
            self.from_date = from_date
            self.till_date = till_date
        if depends_on and isinstance(depends_on, Task):
            self.depends_on = depends_on

    def __repr__(self):
        return "Task: %s" % self.title

