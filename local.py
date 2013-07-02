#!/usr/bin/python

from ganttchart import chart, task, category, render
import re, logger, datetime
from wikiapi import soap
from utils import *

colors = [
        "#00CCFF", "#CCFFFF", "#88FFA4", "#FFFF99",  
        "#99CCFF", "#FF99CC", "#CC99FF", "#FFCC99",  
        "#3366FF", "#33CCCC", "#99CC00", "#FFCC00",
        "#FF9900", "#FF6600", "#8282D0", "#48B5A7",  
        "#477E2A", "#2DAFC4", "#D7A041", "#986E25",  
        "#993300", "#993366", "#3670A3", "#A33663"]

predefined = {"Bench": "#FF8080", "Vacation": "#D0D0D0", "Training": "#A8D237", "Ready": "#F88237"}
categories = {}
color_index = 0
    
def remove_non_ascii(s):
    return "".join(i for i in s if ord(i) < 128)

def get_category(name):
    global color_index, stats

    if name not in categories:
        if name in predefined:
            c = category.Category(name if name != "Ready" else "Ready for a new project", predefined[name], True)
        else:
            c = category.Category(name, colors[color_index])
            color_index += 1
        categories[name] = c

    if categories[name].is_predefined:
        stats[name] = (stats[name] + 1) if name in stats else 0
    return categories[name]

def make_macro(name):
    return "<ac:macro ac:name=\"%s\">([^m]|m[^a]|ma[^c]|mac[^r]|macr[^o])+</ac:macro>" % name

def parse_table(page, table_title, chart, errors=None):
    global stats

    pattern = re.compile("<table id=\"%s\"[^>]*><tbody>([^<]|<[^/]|</[^t]|</t[^b])*</tbody>" % table_title, re.MULTILINE)
    found = pattern.search(page)
    result = True
    if found:
        now = datetime.date.today()
        from_cut = de_weekend(now - datetime.timedelta(days=30))
        table = found.group(1)

        LOGGER.debug("Tabular data found for %s: %s in %s" % (table_title, table, page))

        owners = {}
        max_date = datetime.date.min
        for line in remove_non_ascii(table).split("\n"):
            LOGGER.debug(line)
            try:
                (cat, pool, owner, from_date, till_date) = line.split(",")
            except:
                LOGGER.error("Unable to parse line: %s" % line)
                if line:
                    errors.append("Unable to parse line: '%s'" % line)
                continue
            if cat == "Category":
                continue
            cat = get_category(cat)
            pool = pool.strip()
            owner = owner.strip()
            
            if owner not in owners.keys():
                owners[owner] = {"counter": 0, "last_date": datetime.date.min, "pool": pool}
            owner_data = owners[owner]    

            try:
                t = task.Task("", cat, pool, owner, from_date, till_date)
            except Exception, e:
            	errors.append("%s: '%s'" % (owner, e))
            	result = False
            	continue

            if t.till_date > max_date:
                max_date = t.till_date

            if t.from_date < from_cut and t.till_date > from_cut:
                t.from_date = from_cut

            if t and t.till_date >= now:
                chart.tasks.append(t)
                owner_data["counter"] += 1

            if t.till_date > owner_data["last_date"]:
                owner_data["last_date"] = t.till_date

        for o in owners:
            data = owners[o]
            if data["counter"]:
                continue
            if max_date - data["last_date"] <= datetime.timedelta(days=1):
                max_date = now + datetime.timedelta(weeks=2)

            chart.tasks.append(task.Task("", get_category("Bench"), data["pool"], o, 
                data["last_date"] + datetime.timedelta(days=1), max_date))

        return result
                
def replace_table(page, table_title, chart):
    pattern = re.compile("{csv[^}]+id=%s}([^{]*){csv}" % table_title)
    s = "{csv:output=wiki|id=%s}\nCategory, Pool, Owner, Start, End\n" % table_title
    for t in sorted(chart.tasks):
        s += t.to_csv() + "\n"
    s += "{csv}"

    return pattern.sub(s, page)

if __name__ == "__main__":
    LOGGER = logger.make_custom_logger()
    config = get_config()

    wiki_api = soap.api(config["wiki_soap"])

    wiki_api.connect(config["wiki_login"], config["wiki_password"])
    #page = wiki_api.get_page("CCCOE", "Resources Utilization")
    page = wiki_api.render_content(wiki_api.get_page("~nbogdanov", "Embedding test"))
    LOGGER.debug("Rendered page: %s" % page)

    for location in ["Embedded"]:
        LOGGER.info("Generating chart for location: %s" % location)
        c = chart.OffsetGanttChart("Test Chart")
        parse_table(page, location, c) 

        r = render.Render(600)
        data = r.process(c)

        write_file("out.png", data, "wb")

