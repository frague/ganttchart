#!/usr/bin/python

from datetime import datetime
from exceptions import *
import Image, ImageDraw
from random import randint as rint
from logging import getLogger

import category
import task

LOGGER = getLogger("frague")

class GanttChart:
    """ Represents Gantt Chart """
    def __init__(self, title):
        self.title = title
        self.tasks = []
        LOGGER.debug("New Chart created \"%s\"" % self)
        
    def __repr__(self):
        return "Gantt Chart: %s" % self.title

    def get_height(self, render):
        tasks_height = render.task_height * len(self.tasks)
        return 90 + tasks_height

    def build(self, render):
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
                # Tasks
                for d in sorted(owner_tasks.iterkeys()):
                    for task in owner_tasks[d]:
                    	render.draw_task(task, y)
                    	y += render.task_height
                i += 1


class PlainGanttChart(GanttChart):
    """ Single line per user chart """
    
    def get_height(self, render):
        tasks_height = render.task_height * len(render.tasks_by_owners.keys())
        return 90 + tasks_height

    def build(self, render):
        i = 0
        y = 20
        for pool in sorted(render.owners_by_pools.iterkeys()):
            b = y - 2 + (render.task_height if i > 0 else 0)
            for n in sorted(render.owners_by_pools[pool]):
                y = 20 + render.task_height * i 
                owner_tasks = render.tasks_by_owners[n]
                if i % 2:
                    render.opaque_rectangle(8, y - 1, 11 + render.left_offset + render.active_width, render.task_height - 1, "#0040FF", 32)
                render.text(10, y - 2, n)
                for d in sorted(owner_tasks.iterkeys()):
                    for task in owner_tasks[d]:
                        render.draw_task(task, y)
                i += 1
            render.border(pool, b)

