#!/usr/bin/python

from exceptions import *
from logging import getLogger

LOGGER = getLogger()

class Category:
    """ Represents tasks category """
    def __init__(self, title, color, is_predefined=False):
        self.title = title
        self.color = color
        self.is_predefined = is_predefined
        LOGGER.debug("New category created \"%s\"" % self)

    def __repr__(self):
        return "Category: %s (%s)" % (self.title, self.color)
