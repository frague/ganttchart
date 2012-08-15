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
        self.task_height = 14
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

    def _draw_task(self, task, coords, offset, y):
        x = offset + coords[task.from_date]
        w = int(coords[task.till_date] - coords[task.from_date] + self.day_length)
        self._box(x, y, w, self.task_height - 4)
        self.draw.rectangle((x + 1, y + 1, x + w - 1, y + self.task_height - 5), task.category.color)

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
        self._box(20 + left_offset, 20, active_width, self.height - 88, "#E0E0E0")
        
        days = []
        d = min_date
        while d <= max_date:
            if d.weekday() not in [5, 6]:
                days.append(d)
            d += datetime.timedelta(days=1)
        
        coords = {}
        self.day_length = active_width / float(len(days))
        for i in range(0, len(days)):
            coords[days[i]] = int(i * self.day_length)

        visible = 1
        while visible * self.day_length < 20:
            visible += 1

        for i in range(0, int(math.ceil(len(days) / float(visible)))):
            x = coords[days[i * visible]] + 20 + left_offset

            self.draw.line((x, 20, x, self.height - 68), "#F0F0F0")
            self._vert_text(x - 5, self.height - 60, printable_date(days[i * visible]))
        #self._vert_text(20 + left_offset + active_width - 5, self.height - 60, printable_date(max_date))

        i = 0
        for n in tasks_by_owners.keys():
            y = 20 + self.task_height * i 
            self._text(10, y - 2, n)
            for t in tasks_by_owners[n]:
                self._draw_task(t, coords, 20 + left_offset, y)
                y += self.task_height

            i += len(tasks_by_owners[n])

        self.image.save("out.png", "PNG")
