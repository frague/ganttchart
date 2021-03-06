#!/usr/bin/python

from ganttchart import chart, task, category, render, exceptions, datasource
import re, logger, datetime
from wikiapi import xmlrpc
from utils import *


def make_macro(name):
    return "<ac:macro ac:name=\"%s\">([^m]|m[^a]|ma[^c]|mac[^r]|macr[^o])+</ac:macro>" % name

def csv_pattern(name):
	return re.compile("(<ac:parameter ac:name=\"id\">%s</ac:parameter>([^<]|<[^\!])*<\!\[CDATA\[)(([^\]]|\][^\]])*)(\]\]>)" % (name), re.MULTILINE)

# Searches for inline csv block on the page
# and tries to parse it
def parse_table(page, table_title, chart):
    global stats, errors

    pattern = csv_pattern(table_title)
    found = pattern.search(page)
    if found:
        table = found.group(3)

        LOGGER.debug("CSV data found for %s: %s" % (table_title, table))

        source = datasource.CsvDataSource()
        source.parse(table, chart)
        errors += source.errors
        stats = source.stats

    return len(source.errors) == 0
                

# Replaces inline csv data with updated
def replace_table(text, table_title, chart):
    pattern = csv_pattern(table_title)
    found = pattern.search(text)
    if not found:
    	return text

    s = "Category, Pool, Owner, Start, End\n"
    for t in sorted(chart.tasks):
        s += t.to_csv() + "\n"

    result = pattern.sub("%s%s%s" % (found.group(1), s, found.group(5)), text)
    return result

if __name__ == "__main__":
    LOGGER = logger.make_custom_logger()
    config = get_config()

    wiki_api = xmlrpc.api(config["wiki_xmlrpc"])
    wiki_api.connect(config["wiki_login"], config["wiki_password"])
    page = wiki_api.get_page("CCCOE", "Resources Utilization")

    # Removing errors block
    page["content"] = re.sub(make_macro("warning"), "", page["content"])
    errors = []

    LOGGER.debug(page["content"])

    try:
    	cache_date = datetime.datetime.strptime(read_file("updated.txt"), "%x %X")
    except ValueError:
    	cache_date = datetime.datetime.min
    	LOGGER.error("Unable to read date cache")

    now = datetime.datetime.utcnow()
    wiki = datetime.datetime.strptime(str(page["modified"]), "%Y%m%dT%H:%M:%S") + datetime.timedelta(hours=7)    # TZ compensation hack

    LOGGER.debug("Dates: cache=%s, now=%s, wiki=%s" % (cache_date, now, wiki))

    # If no changes happened to the page on the same day - no charts updates required
    if wiki <= cache_date and now.date() == cache_date.date():
    	LOGGER.info("No page/schemes updates needed")
    	exit() 

    global_stats = {}

    locations = ["Saratov", "Kharkov", "NN", "Poznan", "Moscow"]
    for location in locations:
        stats = {}

        LOGGER.info("Generating chart for location: %s" % location)
        c = chart.OffsetGanttChart("Test Chart")
        
        # If csv section parsing succeeds ...
        if parse_table(page["content"], location, c):
            # update it with the data recalculated
            page["content"] = replace_table(page["content"], location, c)
            # render chart image
            r = render.Render(600)
            image = r.process(c)
            # and upload it to the wiki page
            wiki_api.upload_attachment(page["id"], location.strip() + ".png", "image/png", image)

        global_stats[location] = stats
        LOGGER.debug("Stats for %s: %s" % (location, stats))

    # Updating cache dates
    write_file("updated.txt", (now + datetime.timedelta(minutes=10)).strftime("%x %X"))
    page["content"] = re.sub("Last update: [^<]*", "Last update: %s" % datetime.datetime.now().strftime("%d/%m/%Y %H:%I"), page["content"])

    # Bench Chart
    benches = [str(global_stats[l]["Bench"]) if "Bench" in global_stats[l] else "0" for l in locations]
    page["content"] = re.sub("chd=t:[^&]+", "chd=t:%s" % ",".join(benches), page["content"])
    page["content"] = re.sub("chl=[^&]+", "chl=%s" % "|".join(benches), page["content"])

    if errors:
        LOGGER.error(errors)
        errors_list = "<ac:macro ac:name=\"warning\"><ac:rich-text-body><strong>Parsing errors:</strong><br /><p><ul>%s</ul></p></ac:rich-text-body></ac:macro>" % ("\n".join(["<li> %s</li>" % e for e in errors]))
        page["content"] = re.sub("(%s)" % make_macro("info"), "\\1%s" % errors_list, page["content"])

    # Update wiki page contents
    wiki_api.update_page(page, True)
