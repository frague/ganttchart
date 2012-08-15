#!/usr/bin/python

from datetime import datetime
from exceptions import *
import Image, ImageDraw, ImageFont, ImageOps
from random import randint as rint

import chart
import category
import task

class Render:
    """ Renders Gantt Chart as image"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.font = ImageFont.truetype("/home/nick/dev/gantt/ganttchart/fonts/Cuprum-Regular.ttf", 12)
        self.image = Image.new("RGBA", (self.width, self.height), "#FFFFFF")
        self.draw = ImageDraw.Draw(self.image)

    def _text(self, x, y, text, fill="#000000"):
        self.draw.text((x, y), text, font=self.font, fill=fill)

    def _vert_text(self, x, y, text, fill="#000000"):
        tmp_image = Image.new("RGBA", self.font.getsize(text))
        d = ImageDraw.Draw(tmp_image)
        d.text( (0, 0), text,  font=self.font, fill=fill)
        rotated = tmp_image.rotate(90,  expand=1)
        self.image.paste(rotated, (x, y), rotated)

    def _box(self, x, y, width, height, fill="#000000"):
        self.draw.rectangle((x, y, x + width, y + height), fill=fill)

    def process(self, chart): 

        self.image.save("out.png", "PNG")

