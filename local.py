#!/usr/bin/python

from ganttchart import chart, datasource, render
from logger import make_custom_logger
from utils import *

if __name__ == "__main__":
    LOGGER = make_custom_logger()

    data = read_file("test.csv")
    LOGGER.debug("Rendered page: %s" % data)

    source = datasource.CsvDataSource()
#    c = chart.OffsetGanttChart("Test Chart")
    c = chart.GanttChart("Test Chart")
    source.parse(data, c)
    r = render.Render(600)
    image_rendered = r.process(c)

    write_file("out.png", image_rendered, "wb")

