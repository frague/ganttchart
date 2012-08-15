#!/usr/bin/python

from ganttchart import chart, task, category, render

if __name__ == "__main__":
    c = chart.GanttChart("Test")
    r = render.Render(600, 400)
    r.process(c)
