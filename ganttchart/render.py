#!/usr/bin/python

from datetime import datetime
from exceptions import *
import Image, ImageDraw, ImageFont
from random import randint as rint

import chart
import category
import task

class Render:
    """ Renders Gantt Chart as image"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = ImageFont.truetype("/home/nick/dev/gantt/ganttchart/fonts/Cuprum-Regular.ttf", 15)
        self.image = Image.new("RGB", (self.width, self.height), "#FFFFFF")
        self.draw = ImageDraw.Draw(self.image)

    def process(self, chart):    
        r,g,b = rint(0,255), rint(0,255), rint(0,255)
        dr = (rint(0,255) - r)/300.
        dg = (rint(0,255) - g)/300.
        db = (rint(0,255) - b)/300.
        for i in range(300):
            r,g,b = r+dr, g+dg, b+db
            #self.draw.line((i,0,i,300), fill=(int(r),int(g),int(b)))

        self.draw.text((10, 25), "world", font=self.font, fill=128)
        self.image.save("out.png", "PNG")

