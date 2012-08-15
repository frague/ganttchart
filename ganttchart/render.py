#!/usr/bin/python

from datetime import datetime
from exceptions import *
from utils import *
import Image, ImageDraw, ImageFont, ImageOps

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
        self.draw.line((x, y, x, y + height), fill=fill)
        self.draw.line((x, y + height, x + width, y + height), fill=fill)
        self.draw.line((x + width, y + height, x + width, y), fill=fill)
        self.draw.line((x + width, y, x, y), fill=fill)

    def process(self, chart): 
        min_date = datetime.datetime.max
        max_date = datetime.datetime.min
        tasks_by_owners = {}
        left_offset = 0
        for task in chart.tasks:
            if task.from_date < min_date:
                min_date = task.from_date
            if task.till_date > max_date:
                max_date = task.till_date
            owner = task.owner
            if owner not in tasks_by_owners:
                tasks_by_owners[owner] = []
            tasks_by_owners[owner].append(task)
            o = self.font.getsize(owner)[0]
            if o > left_offset:
                left_offset = o

        self._box(20 + left_offset, 20, self.width - left_offset - 30, self.height - 30, "#E0E0E0")
        i = 0
        for n in tasks_by_owners.keys():
            self._text(10, 20 * i, n)
            i += 1
        self.image.save("out.png", "PNG")

