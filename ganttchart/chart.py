#!/usr/bin/python

from datetime import datetime, date, timedelta
from exceptions import *
import Image, ImageDraw
from random import randint as rint
from logging import getLogger

import category
import task

LOGGER = getLogger()

class GanttChart:
    """ Represents Gantt Chart """
    def __init__(self, title):
        self.title = title
        self.tasks = []
        LOGGER.debug("New Chart created \"%s\"" % self)
        
    def __repr__(self):
        return "Gantt Chart: %s" % self.title

    def get_height(self, render):
        return 90 + self._tasks_height(render)

    def _tasks_height(self, render):
        return render.task_height * len(self.tasks)

    def get_category(self, name):
    	for t in self.tasks:
    	    if t.category.title == name:
    	        return t.category
    	return category.Category("Bench", "#FFFF00")
    
    def draw(self, render):
        i = 0
        y = 20
        # Pools
        for pool in sorted(render.owners_by_pools.iterkeys()):
            render.border(pool, y - (2 if i else 0))
            # Users
            for n in sorted(render.owners_by_pools[pool]):
                owner_tasks = render.tasks_by_owners[n]
                tasks_num = len(owner_tasks)
                if i % 2:
                    render.opaque_rectangle(8, y - 1, 11 + render.left_offset + render.active_width, render.task_height * tasks_num - 1, "#0040FF", 32)
                render.text(10, y - 2, n)
                # Tasks dates
                for d in sorted(owner_tasks.iterkeys()):
                    # Tasks
                    for task in owner_tasks[d]:
                    	render.draw_task(task, y)
                    	y += render.task_height
                i += 1


class PlainGanttChart(GanttChart):
    """ Single line per user chart """
    
    def _tasks_height(self, render):
        return render.task_height * len(render.tasks_by_owners.keys())

    def draw(self, render):
        i = 0
        y = 20
        # Pools
        for pool in sorted(render.owners_by_pools.iterkeys()):
            b = y - 2 + (render.task_height if i > 0 else 0)
            # Users
            for n in sorted(render.owners_by_pools[pool]):
                y = 20 + render.task_height * i 
                owner_tasks = render.tasks_by_owners[n]
                if i % 2:
                    render.opaque_rectangle(8, y - 1, 11 + render.left_offset + render.active_width, render.task_height - 1, "#0040FF", 32)
                render.text(10, y - 2, n)
                # Tasks dates
                for d in sorted(owner_tasks.iterkeys()):
                    # Tasks per date
                    for task in owner_tasks[d]:
                        render.draw_task(task, y)
                i += 1
            render.border(pool, b)

class OffsetGanttChart(GanttChart):
    """ Tasks are rendered with tiny vertical offset """
    def __init__(self, title):
    	self.vertical_offset = 4
    	GanttChart.__init__(self, title)
    
    def _tasks_height(self, render):
        owners_num = len(render.tasks_by_owners.keys())
        return render.task_height * owners_num + (len(self.tasks) - owners_num) * self.vertical_offset

    def draw(self, render):
        i = 0
        y = 20
        today = date.today()
        # Pools
        for pool in sorted(render.owners_by_pools.iterkeys()):
            render.border(pool, y - (2 if i else 0))
            # Users
            for n in sorted(render.owners_by_pools[pool]):
                owner_tasks = render.tasks_by_owners[n]
                tasks_num = len(owner_tasks)
                if i % 2:
                    render.opaque_rectangle(8, y - 1, 11 + render.left_offset + render.active_width, render.task_height + self.vertical_offset * (tasks_num - 1) - 1, "#0040FF", 32)
                render.text(10, y - 2, n)
                # Tasks dates
                d, t = None, None
                for d in sorted(owner_tasks.iterkeys()):
                    # Tasks
                    for t in owner_tasks[d]:
                    	render.draw_task(t, y)
                    	y += self.vertical_offset
                #if t.till_date < today:
                #    t1 = task.Task("", self.get_category("Bench"), t.pool, t.owner, render.de_weekend(t.till_date + timedelta(days=1)), render.max_date)
                #    render.draw_task(t1, y - self.vertical_offset, 64)
                    
                i += 1
                y += render.task_height - self.vertical_offset
