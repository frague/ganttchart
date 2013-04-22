#!/usr/bin/python

from ganttchart import chart, task, category, render, exceptions
import re, logger, datetime
from wikiapi import xmlrpc
from utils import *

colors = [
        "#00CCFF", "#CCFFFF", "#88FFA4", "#FFFF99",  
        "#99CCFF", "#FF99CC", "#CC99FF", "#FFCC99",  
        "#3366FF", "#33CCCC", "#99CC00", "#FFCC00",
        "#FF9900", "#FF6600", "#666699", "#969696",  
        "#003300", "#339966", "#003300", "#333300",  
        "#993300", "#993366", "#333399", "#333333"]

predefined = {"Bench": "#FF8080", "Vacation": "#D0D0D0"}
categories = {}
color_index = 0
    
def remove_non_ascii(s):
    return "".join(i for i in s if ord(i) < 128)

def get_category(name):
    global color_index

    if name not in categories:
        if name in predefined:
            color = predefined[name]
        else:
            color = colors[color_index]
            color_index += 1
        categories[name] = category.Category(name, color)
    return categories[name]

def parse_table(page, table_title, chart, errors=None):
    pattern = re.compile("{csv[^}]+id=%s}([^{]*){csv}" % table_title)
    found = pattern.search(page)
    result = True
    if found:
        now = datetime.date.today()
        from_cut = de_weekend(now - datetime.timedelta(days=30))
        table = found.group(1)
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

def make_macro(name):
    return "<ac:macro ac:name=\"%s\">([^m]|m[^a]|ma[^c]|mac[^r]|macr[^o])+</ac:macro>" % name

if __name__ == "__main__":
    LOGGER = logger.make_custom_logger()
    config = get_config()

    wiki_api = xmlrpc.api(config["wiki_xmlrpc"])

    wiki_api.connect(config["wiki_login"], config["wiki_password"])
    page = wiki_api.get_page("CCCOE", "Resources Utilization")

    # Removing errors block
    # <ac:macro ac:name="warning"><ac:rich-text-body><p>&nbsp;</p></ac:rich-text-body></ac:macro>
    page["content"] = re.sub(make_macro("warning"), "", page["content"])
    errors = []

    try:
    	cache_date = datetime.datetime.strptime(read_file("updated.txt"), "%x %X")
    except ValueError:
    	cache_date = datetime.datetime.min
    	LOGGER.error("Unable to read date cache")
    now = datetime.datetime.utcnow()
    wiki = datetime.datetime.strptime(str(page["modified"]), "%Y%m%dT%H:%M:%S") + datetime.timedelta(hours=7)    # TZ compensation hack

    LOGGER.debug("Dates: cache=%s, now=%s, wiki=%s" % (cache_date, now, wiki))

    if wiki <= cache_date and now.date() == cache_date.date():
    	LOGGER.info("No page/schemes updates needed")
    	exit() 

    for location in ["Saratov", "Kharkov", "Moscow", "Poznan", "NN"]:
        LOGGER.info("Generating chart for location: %s" % location)
        c = chart.OffsetGanttChart("Test Chart")
        
        if parse_table(page["content"], location, c, errors):
            page["content"] = replace_table(page["content"], location, c)
            r = render.Render(600)
            data = r.process(c)
            wiki_api.upload_attachment(page["id"], location.strip() + ".png", "image/png", data)

    write_file("updated.txt", (now + datetime.timedelta(minutes=10)).strftime("%x %X"))
    page["content"] = re.sub("Last update: [^<]*", "Last update: %s" % datetime.datetime.now().strftime("%d/%m/%Y %H:%I"), page["content"])

    if errors:
        LOGGER.error(errors)
        errors_list = "<ac:macro ac:name=\"warning\"><ac:rich-text-body><strong>Parsing errors:</strong><br /><p><ul>%s</ul></p></ac:rich-text-body></ac:macro>" % ("\n".join(["<li> %s</li>" % e for e in errors]))
        page["content"] = re.sub("(%s)" % make_macro("info"), "\\1%s" % errors_list, page["content"])

    wiki_api.update_page(page, True)
