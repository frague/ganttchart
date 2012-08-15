#!/usr/bin/python

import datetime, math
from exceptions import *
from utils import *
import Image, ImageDraw, ImageFont, ImageOps

import chart
import category
import task

class Render:
    """ Renders Gantt Chart as image"""
    def __init__(self, width):
        self.width = width
        self.task_height = 20
        self.font = ImageFont.truetype("/home/nick/dev/gantt/ganttchart/fonts/Cuprum-Regular.ttf", 12)

    def _text(self, x, y, text, fill="#000000"):
        self.draw.text((x, y), text, font=self.font, fill=fill)

    def _vert_text(self, x, y, text, fill="#000000"):
        (w, h) = self.font.getsize(text)
        tmp_image = Image.new("RGBA", (w + 2, h))
        d = ImageDraw.Draw(tmp_image)
        d.text( (2, 0), text,  font=self.font, fill=fill)
        rotated = tmp_image.rotate(90,  expand=1)
        self.image.paste(rotated, (x, y), rotated)

    def _box(self, x, y, width, height, fill="#000000"):
        self.draw.line((x, y, x, y + height), fill=fill)
        self.draw.line((x, y + height, x + width, y + height), fill=fill)
        self.draw.line((x + width, y + height, x + width, y), fill=fill)
        self.draw.line((x + width, y, x, y), fill=fill)

    def process(self, chart):
        self.height = 70 + self.task_height * (1 + len(chart.tasks))
        self.image = Image.new("RGBA", (self.width, self.height), "#FFFFFF")
        self.draw = ImageDraw.Draw(self.image)

        min_date = datetime.date.max
        max_date = datetime.date.min
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

        active_width = self.width - left_offset - 30
        self._box(20 + left_offset, 20, active_width, self.height - 90, "#E0E0E0")
        
        i = 1
        for n in tasks_by_owners.keys():
            self._text(10, self.task_height * i, n)
            i += len(tasks_by_owners[n])

        days = []
        d = min_date
        while d < max_date:
            if not d.weekday in (5, 6):
                days.append(d)
            d += datetime.timedelta(days=1)
        
        coords = {}
        day_length = active_width / len(days)
        for i in range(0, len(days)):
            coords[days[i]] = int(i * day_length)

        visible = 1
        while visible * day_length < 20:
            visible += 1

        for i in range(0, int(math.ceil(len(days) / visible))):
            x = coords[days[i * visible]] + 20 + left_offset

            self.draw.line((x, 20, x, self.height - 70), "#F0F0F0")
            self._vert_text(x - 5, self.height - 60, printable_date(days[i]))

        
        
        self.image.save("out.png", "PNG")
