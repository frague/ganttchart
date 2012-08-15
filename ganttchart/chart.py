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
        self.categories = {}
        self.tasks = {}
        
        def __repr__(self):
            return "Gantt Chart: %s" % self.title

        def render(self):
            img = Image.new("RGB", (300,300), "#FFFFFF")
            draw = ImageDraw.Draw(img)

            r,g,b = rint(0,255), rint(0,255), rint(0,255)
            dr = (rint(0,255) - r)/300.
            dg = (rint(0,255) - g)/300.
            db = (rint(0,255) - b)/300.
            for i in range(300):
                r,g,b = r+dr, g+dg, b+db
                draw.line((i,0,i,300), fill=(int(r),int(g),int(b)))

            img.save("out.png", "PNG")

