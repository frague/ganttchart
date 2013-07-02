#!/usr/bin/python

from exceptions import *
from logging import getLogger

LOGGER = getLogger()
category_color_index = 0
category_colors = [
        "#00CCFF", "#CCFFFF", "#88FFA4", "#FFFF99",  
        "#99CCFF", "#FF99CC", "#CC99FF", "#FFCC99",  
        "#3366FF", "#33CCCC", "#99CC00", "#FFCC00",
        "#FF9900", "#FF6600", "#8282D0", "#48B5A7",  
        "#477E2A", "#2DAFC4", "#D7A041", "#986E25",  
        "#993300", "#993366", "#3670A3", "#A33663",
        "#D9ECA7", "#F3F6B7", "#F8C592", "#F4A586",
        "#00BFFF", "#00DED1", "#00FA9A", "#AFEEEE", 
        "#F5DEB3", "#FFD700", "#FA8072", "#E6E6FA"
        ]

def pick_color():
    global category_colors, category_color_index

    result = category_colors[category_color_index]
    category_color_index += 1
    if category_color_index == len(category_colors):
        category_color_index = 0
    return result

# Represents tasks category
class Category:
    def __init__(self, title, color=None, is_predefined=False):
        self.replaces = {"Ready for a new project": "Ready"}
        self.title = title
        if color:
            self.color = color
        else:
            self.color = pick_color()
        self.is_predefined = is_predefined
        LOGGER.debug("New category created \"%s\"" % self)

    def __repr__(self):
        return "Category: %s (%s)" % (self.title, self.color)

    @property
    def smart_title(self):
        if self.is_predefined:
            if self.title in self.replaces.keys():
                return self.replaces[self.title]
        return self.title
