#!/usr/bin/python

from ganttchart import chart, task, category, render, exceptions
import re, logger, datetime
from exceptions import *
from logging import getLogger
from utils import *

LOGGER = getLogger()

# Extended owner data
class OwnerData:
    def __init__(self, pool, counter=0, last_date=None):
        self.counter = counter
        self.last_date = last_date if last_date is not None else datetime.date.min
        self.pool = pool

class BaseDataSource:
    predefined = {"Bench": "#FF8080", "Vacation": "#D0D0D0", "Training": "#A8D237", "Ready": "#F88237"}
    
    def __init__(self):
        self.categories = {}
        self.owners = {}
        self.stats = {}
        self.max_date = datetime.date.min
        self.errors = []

        self.now = datetime.date.today()
        self.from_cut = de_weekend(self.now - datetime.timedelta(days=30))

    # Returns category by name. Create new one if never met before
    def _get_category(self, name):
        if name not in self.categories:
            if name in self.predefined:
                c = category.Category(name if name != "Ready" else "Ready for a new project", self.predefined[name], True)
            else:
                c = category.Category(name)
            self.categories[name] = c

        if self.categories[name].is_predefined:
            self.stats[name] = (self.stats[name] + 1) if name in self.stats else 0
        return self.categories[name]

    # Parses the single line of data source
    def _parse_line(self, cat, pool, owner, from_date, till_date):
        LOGGER.debug("Parsing line: %s" % ("|".join([cat, pool, owner, from_date, till_date])))

        # Column names row 
        if cat == "Category":
            return
            
        cat = self._get_category(cat)
        pool = pool.strip()
        owner = owner.strip()
            
        # Extended data for task owner
        if owner not in self.owners.keys():
            self.owners[owner] = OwnerData(pool)
        owner_data = self.owners[owner]    

        try:
            # Trying to create task
            t = task.Task("", cat, pool, owner, from_date, till_date)
        except Exception, e:
            self.errors.append("%s: '%s'" % (owner, e))
            return None

        # Determining max date
        if t.till_date > self.max_date:
            self.max_date = t.till_date

        # Cutting task' from date by cut date
        if t.from_date < self.from_cut and t.till_date > self.from_cut:
            t.from_date = self.from_cut

        if t.till_date > owner_data.last_date:
            owner_data.last_date = t.till_date
        
        # Showing the only active tasks
        if t and t.till_date >= self.now:
            owner_data.counter += 1
            return t
        return None

    # For users with no active tasks create Bench tasks
    def _benchify(self, chart):
        for owner in self.owners:
            owner_data = self.owners[owner]
            if owner_data.counter:
                continue

            if self.max_date - owner_data.last_date <= datetime.timedelta(days=1):
                self.max_date = self.now + datetime.timedelta(weeks=2)

            t = task.Task("", self._get_category("Bench"), owner_data.pool, owner, 
                owner_data.last_date + datetime.timedelta(days=1), self.max_date)
            LOGGER.error("Bench task: %s" % t)
            chart.tasks.append(t)

# Parsing css data
class CsvDataSource(BaseDataSource):
    # Remove all non-ascii chars from the string provided
    def _remove_non_ascii(self, s):
        return "".join(i for i in s if ord(i) < 128)

    # Iterate through data lines and create tasks
    def parse(self, source, chart):
        for line in self._remove_non_ascii(source).split("\n"):
            try:
                (cat, pool, owner, from_date, till_date) = line.split(",")
                t = self._parse_line(cat, pool, owner, from_date, till_date)
            except Exception, e:
                LOGGER.error("Unable to parse line: %s (%s)" % (line, e))
                if line:
                    self.errors.append("Unable to parse line: '%s'" % line)
                continue
            if t:
                chart.tasks.append(t)
        self._benchify(chart)
