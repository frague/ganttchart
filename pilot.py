#!/usr/bin/python

from ganttchart import chart, task, category, render

if __name__ == "__main__":
    c = chart.GanttChart("Test Chart")
    cat1 = category.Category("Heartbeat", "#FF8080")
    cat2 = category.Category("Vacation", "#00FF80")

    c.tasks.append(task.Task("", cat1, "Nick Bogdanov", "06/03/2012", "08/03/2012")) 
    c.tasks.append(task.Task("", cat2, "Nick Bogdanov", "08/06/2012", "08/20/2012")) 

    r = render.Render(600, 400)
    r.process(c)
