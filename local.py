#!/usr/bin/python

from ganttchart import chart, task, category, render
import re, logger, datetime
from wikiapi import xmlrpc
from utils import *

colors = [
        "#00CCFF", "#CCFFFF", "#CCFFCC", "#FFFF99",  
        "#99CCFF", "#FF99CC", "#CC99FF", "#FFCC99",  
        "#3366FF", "#33CCCC", "#99CC00", "#FFCC00",
        "#FF9900", "#FF6600", "#666699", "#969696",  
        "#003300", "#339966", "#003300", "#333300",  
        "#993300", "#993366", "#333399", "#333333"]


def parse_table(page, table_title, chart):
    pattern = re.compile("{csv[^}]+id=%s}([^{]*){csv}" % table_title)
    found = pattern.search(page)
    if found:
        color_index = 0
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
                categories[cat] = category.Category(cat, colors[color_index])
                color_index += 1
            cat = categories[cat]
            chart.tasks.append(task.Task("", cat, pool.strip(), owner.strip(), from_date, till_date)) 

if __name__ == "__main__":
    LOGGER = logger.make_custom_logger()
    config = get_config()

    wiki_api = xmlrpc.api(config["wiki_xmlrpc"])

    wiki_api.connect(config["wiki_login"], config["wiki_password"])
    page = wiki_api.get_page("CCCOE", "Resources Utilization")

    for location in ["Saratov"]:
        LOGGER.info("Generating chart for location: %s" % location)
        c = chart.GanttChart("Test Chart")
        parse_table(page["content"], location, c) 

        r = render.Render(600)
        data = r.process(c)

        write_file("out.png", data, "wb")

