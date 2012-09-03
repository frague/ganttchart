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
        self.task_height = 20
        #self.font_file = "pf_easta_seven_condensed.ttf" #8
        #self.font_file = "PIXEARG_.ttf" #8
        self.font_file = "resource.ttf" #16
        self.font = ImageFont.truetype("%s/fonts/%s" % (os.path.split(os.path.realpath(__file__))[0], self.font_file), 16)

    def _init_image(self, image):
        self.image = image
        self.draw = ImageDraw.Draw(self.image)
        self.draw.fontmode = "1"

    def text(self, x, y, text, fill="#000000"):
        LOGGER.debug("Printing \"%s\" to (%s,%s)" % (text, x, y))
        self.draw.text((x, y), text, font=self.font, fill=fill)

    def vert_text(self, x, y, text, fill="#000000", angle=90):
        LOGGER.debug("Printing vertical \"%s\" to (%s,%s) on %s deg." % (text, x, y, angle))
        (w, h) = self.font.getsize(text)
        tmp_image = Image.new("RGBA", (w + 2, h))
        d = ImageDraw.Draw(tmp_image)
        d.text( (2, 0), text,  font=self.font, fill=fill)
        rotated = tmp_image.rotate(angle,  expand=1)
        self.image.paste(rotated, (x, y), rotated)

    def box(self, x, y, width, height, fill="#000000"):
        LOGGER.debug("Draw rectangle (%s, %s) - (%s, %s)" % (x, y, width, height))
        self.draw.line((x, y, x, y + height), fill=fill)
        self.draw.line((x, y + height, x + width, y + height), fill=fill)
        self.draw.line((x + width, y + height, x + width, y), fill=fill)
        self.draw.line((x + width, y, x, y), fill=fill)

    def opaque_rectangle(self, x, y, width, height, fill="#000000", opacity=128):
        LOGGER.debug("Draw opaque rectangle (%s, %s) - (%s, %s)" % (x, y, width, height))
        color_layer = Image.new("RGBA", self.image.size, fill)
        alpha_mask = Image.new("L", self.image.size, 0)
        alpha_mask_draw = ImageDraw.Draw(alpha_mask)
        alpha_mask_draw.rectangle((x, y, x + width, y + height), opacity)   # Opacity here?
        self._init_image(Image.composite(color_layer, self.image, alpha_mask))

    def draw_task(self, task, y):
        LOGGER.debug("Drawing task: %s" % task)
        x = 20 + self.left_offset + self.coords[task.from_date]
        w = int(self.coords[self._de_weekend(task.till_date, False)] - self.coords[self._de_weekend(task.from_date)] + self.day_length)
        self.opaque_rectangle(x + 1, y + 1, w - 2, self.task_height - 5, task.category.color, 200)
        self.box(x, y, w - 1, self.task_height - 4)
        self.text(x + 2, y - 2, task.category.title)

    def milestone(self, date, fill="#808080", textfill="#808080"):
        if date not in self.coords:
            return
        x = self.coords[date] + 20 + self.left_offset

        self.draw.line((x, 19, x, self.height - 73), fill)
        self.vert_text(x - 8, self.height - 60, printable_date(date), textfill)

    def border(self, text, y, fill="#808080"):
        if y > 20:
            self.draw.line((21 + self.left_offset, y, 19 + self.left_offset + self.active_width, y), fill=fill)
        if text:
            self.vert_text(18 + self.left_offset + self.active_width, y, text, fill=fill, angle=270)

    def _de_weekend(self, d, later=True):
        delta = 7 - d.weekday()
        if delta in [1, 2]:
            d += datetime.timedelta(days=delta) if later else datetime.timedelta(days=delta-3)
        return d

    def process(self, chart):
        self.min_date = datetime.date.max
        self.max_date = datetime.date.min
        self.tasks_by_owners = {}
        self.owners_by_pools = {}
        self.left_offset = 0
        for task in chart.tasks:
            LOGGER.debug("Processing %s" % task)
            if task.from_date < self.min_date:
                self.min_date = task.from_date
            if task.till_date > self.max_date:
                self.max_date = task.till_date

            owner = task.owner
            if owner not in self.tasks_by_owners:
                self.tasks_by_owners[owner] = {}
            if task.from_date not in self.tasks_by_owners[owner]:
                self.tasks_by_owners[owner][task.from_date] = []
            self.tasks_by_owners[owner][task.from_date].append(task)
            
            if task.pool not in self.owners_by_pools:
                self.owners_by_pools[task.pool] = []
            if owner not in self.owners_by_pools[task.pool]:
                self.owners_by_pools[task.pool].append(owner)

            o = self.font.getsize(owner)[0]
            if o > self.left_offset:
                self.left_offset = o

        # Getting chart height
        self.height = chart.get_height(self)

        self._init_image(Image.new("RGBA", (self.width, self.height), "#FFFFFF"))

        self.active_width = self.width - self.left_offset - 30
        self.box(20 + self.left_offset, 18, self.active_width, self.height - 90, "#808080")
        
        days = []
        d = self.min_date
        while d <= self.max_date:
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
            self.milestone(days[i * visible], "#808080" if not i else "#F0F0F0", "#808080")

        today = self._de_weekend(datetime.date.today())
        self.milestone(today, "#FF0000", "#FF0000")

        chart.draw(self)

        output = StringIO.StringIO()
        self.image.save(output, "PNG")
        data = output.getvalue()
        output.close()
        return data
