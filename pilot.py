#!/usr/bin/python

from ganttchart import chart, task, category, render
from wikiapi import xmlrpc
from utils import *
from logger import get_logger
import re

def parse_table(page, table_title, chart):
    #{csv:output=wiki|id=Saratov}
    pattern = re.compile("{csv[^}]+id=%s}([^{]*){csv}" % table_title)
    found = pattern.search(page)
    if found:
        table = found.group(1)
        categories = {}
        for line in table.split("\n"):
            LOGGER.debug(line)
            try:
                (cat, pool, owner, from_date, till_date) = line.split(",")
            except:
                continue
            if cat == "Category":
                continue
            if cat not in categories:
                categories[cat] = category.Category(c, "#808080")
            cat = categories[cat]
            chart.tasks.append(task.Task("", cat, owner, from_date, till_date)) 

if __name__ == "__main__":
    LOGGER = get_logger(__name__)
    config = get_config()

    wiki_api = xmlrpc.api(config["wiki_xmlrpc"])

    wiki_api.connect(config["wiki_login"], config["wiki_password"])
    page = wiki_api.get_page("CCCOE", "Resources Utilization")

    c = chart.GanttChart("Test Chart")
    parse_table(page["content"], "Saratov", c) 
    
    
    """
    cat1 = category.Category("Heartbeat", "#FF8080")
    cat2 = category.Category("Vacation", "#00FF80")
    cat3 = category.Category("Bench", "#0080FF")

    c.tasks.append(task.Task("", cat2, "Nick Bogdanov", "08/06/2012", "08/17/2012")) 
    c.tasks.append(task.Task("", cat3, "Nick Bogdanov", "08/20/2012", "08/24/2012")) 
    c.tasks.append(task.Task("", cat1, "Nick Bogdanov", "06/03/2012", "08/03/2012")) 
    
    c.tasks.append(task.Task("", cat1, "Dmitry Russkikh", "06/03/2012", "08/03/2012")) 
    c.tasks.append(task.Task("", cat2, "Max Lvov", "08/06/2012", "08/26/2012")) 
    c.tasks.append(task.Task("", cat1, "Max Lvov", "06/03/2012", "08/03/2012")) 
    c.tasks.append(task.Task("", cat1, "Roman Bogorodskiy", "06/03/2012", "08/03/2012")) 
    """

    r = render.Render(600)
    r.process(c)
