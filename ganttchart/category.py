#!/usr/bin/python

from exceptions import *
from logging import getLogger

LOGGER = getLogger("frague")

class Category:
    """ Represents tasks category """
    def __init__(self, title, color):
        self.title = title
        self.color = color
        LOGGER.debug("New category created \"%s\"" % self)

    def __repr__(self):
        return "Category: %s (%s)" % (self.title, self.color)
