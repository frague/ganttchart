#!/usr/bin/python

import datetime, math, os, logging, StringIO
import Image, ImageDraw, ImageFont, ImageOps
from exceptions import *
from utils import *

import chart, category, task

LOGGER = logging.getLogger("frague")

class Render:
    """ Renders Gantt Chart as image"""
    def __init__(self, width):
        self.width = width
        self.task_height = 14
        #self.font_file = "pf_easta_seven_condensed.ttf" #8
        #self.font_file = "PIXEARG_.ttf" #8
        self.font_file = "resource.ttf" #16
        self.font = ImageFont.truetype("%s/fonts/%s" % (os.path.split(os.path.realpath(__file__))[0], self.font_file), 16)

    def _text(self, x, y, text, fill="#000000"):
        LOGGER.debug("Printing \"%s\" to (%s,%s)" % (text, x, y))
        self.draw.text((x, y), text, font=self.font, fill=fill)

    def _vert_text(self, x, y, text, fill="#000000", angle=90):
        LOGGER.debug("Printing vertical \"%s\" to (%s,%s) on %s deg." % (text, x, y, angle))
        (w, h) = self.font.getsize(text)
        tmp_image = Image.new("RGBA", (w + 2, h))
        d = ImageDraw.Draw(tmp_image)
        d.text( (2, 0), text,  font=self.font, fill=fill)
        rotated = tmp_image.rotate(angle,  expand=1)
        self.image.paste(rotated, (x, y), rotated)

    def _box(self, x, y, width, height, fill="#000000"):
        LOGGER.debug("Draw rectangle (%s, %s) - (%s, %s)" % (x, y, width, height))
        self.draw.line((x, y, x, y + height), fill=fill)
        self.draw.line((x, y + height, x + width, y + height), fill=fill)
        self.draw.line((x + width, y + height, x + width, y), fill=fill)
        self.draw.line((x + width, y, x, y), fill=fill)

    def _draw_task(self, task, y):
        x = 20 + self.left_offset + self.coords[task.from_date]
        w = int(self.coords[task.till_date] - self.coords[task.from_date] + self.day_length)
        self._box(x, y, w - 1, self.task_height - 4)
        self.draw.rectangle((x + 1, y + 1, x + w - 2, y + self.task_height - 5), task.category.color)
        self._text(x + 2, y - 2, task.category.title)

    def _milestone(self, date, fill="#808080", textfill="#808080"):
        if date not in self.coords:
            return
        x = self.coords[date] + 20 + self.left_offset

        self.draw.line((x, 21, x, self.height - 70), fill)
        self._vert_text(x - 5, self.height - 60, printable_date(date), textfill)

    def _border(self, text, y, fill="#808080"):
        if y > 20:
            self.draw.line((21 + self.left_offset, y, 18 + self.left_offset + self.active_width, y), fill=fill)
        if text:
            self._vert_text(18 + self.left_offset + self.active_width, y, text, fill=fill, angle=270)

    def process(self, chart):
        min_date = datetime.date.max
        max_date = datetime.date.min
        tasks_by_owners = {}
        owners_by_pools = {}
        self.left_offset = 0
        for task in chart.tasks:
            LOGGER.debug("Processing %s" % task)
            if task.from_date < min_date:
                min_date = task.from_date
            if task.till_date > max_date:
                max_date = task.till_date
            owner = task.owner
            if owner not in tasks_by_owners:
                tasks_by_owners[owner] = {}
            tasks_by_owners[owner][task.from_date] = task
            
            if task.pool not in owners_by_pools:
                owners_by_pools[task.pool] = []
            if owner not in owners_by_pools[task.pool]:
                owners_by_pools[task.pool].append(owner)

            o = self.font.getsize(owner)[0]
            if o > self.left_offset:
                self.left_offset = o

        self.height = 70 + self.task_height * (1 + len(tasks_by_owners.keys()))
        self.image = Image.new("RGBA", (self.width, self.height), "#FFFFFF")
        self.draw = ImageDraw.Draw(self.image)
        self.draw.fontmode = "1"

        self.active_width = self.width - self.left_offset - 30
        self._box(20 + self.left_offset, 20, self.active_width, self.height - 88, "#808080")
        
        days = []
        d = min_date
        while d <= max_date:
            if d.weekday() not in [5, 6]:
                days.append(d)
            d += datetime.timedelta(days=1)
        
        self.coords = {}
        self.day_length = self.active_width / float(len(days))
        for i in range(0, len(days)):
            self.coords[days[i]] = int(i * self.day_length)

        visible = 1
        while visible * self.day_length < 20:
            visible += 1

        for i in range(0, int(math.ceil(len(days) / float(visible)))):
            self._milestone(days[i * visible], "#808080" if not i else "#F0F0F0", "#808080")
        today = datetime.date.today()
        delta = 7 - today.weekday()
        if delta in [1, 2]:
            today += datetime.timedelta(days=delta)
        self._milestone(today, "#FF0000", "#FF0000")

        i = 0
        y = 20
        for pool in sorted(owners_by_pools.iterkeys()):
            b = y - 2 + (self.task_height if i > 0 else 0)
            for n in sorted(owners_by_pools[pool]):
                y = 20 + self.task_height * i 
                self._text(10, y - 2, n)
                owner_tasks = tasks_by_owners[n]
                for d in sorted(owner_tasks.iterkeys()):
                    t = owner_tasks[d]
                    self._draw_task(t, y)
                self._border(None, y - 2, "#F0F0F0")

                i += 1
            self._border(pool, b)

        output = StringIO.StringIO()
        self.image.save(output, "PNG")
        data = output.getvalue()
        output.close()
        return data
