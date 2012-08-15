#!/usr/bin/python

from exceptions import *

class Category:
    """ Represents tasks category """
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return "Category: %s" % self.title
