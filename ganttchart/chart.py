#!/usr/bin/python

from datetime import datetime
from exceptions import *
import Image, ImageDraw
from random import randint as rint
from logging import getLogger

import category
import task

LOGGER = getLogger("frague")

class GanttChart:
    """ Represents Gantt Chart """
    def __init__(self, title):
        self.title = title
        self.tasks = []
        LOGGER.debug("New Chart created \"%s\"" % self)
        
    def __repr__(self):
        return "Gantt Chart: %s" % self.title

