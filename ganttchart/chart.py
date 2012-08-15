#!/usr/bin/python

from datetime import datetime
from exceptions import *
import Image, ImageDraw
from random import randint as rint

import category
import task

class GanttChart:
    """ Represents Gantt Chart """
    def __init__(self, title):
        self.title = title
        self.tasks = []
        
    def __repr__(self):
        return "Gantt Chart: %s" % self.title

