ganttchart
==========

This library allows to create simple gantt-charts like the one below.
![Gantt chart generated](/out.png "Gantt chart generated")

Data Sources
------------
Only CSV input data format is supported at the moment, however other sources might be added via [DataSource](/ganttchart/datasource.py) base class extension.

Above smaple chart is built with [local.py](/local.py) script with [test.csv](/test.csv) file as a data source.
It has the following structure:
```csv
Category, Pool, Owner, Start, End
Apple,  BA,	James Cook,	24/06/2013,	01/08/2013
Intel,	BA,	James Cook,	2/08/2013,	01/09/2013
Microsoft,	BA,	James Cook,	2/09/2013,	01/10/2013
RnD,	BA,	George Willson,	31/05/2013,	01/10/2013
Vacation,	BA,	George Willson,	2/07/2013,	14/07/2013
......
```
where
* **Category** - projects (differentiated by colour)
* **Pool** - pools of resources (engineering specialities in provided example). All tasks are groupped by pools and sorted by Owner
* **Owner** - assignee
* **Start** - assignment start date
* **End** - assignment end date

Alternative Chart Views
-----------------------
Library supports 3 different views of Gantt Charts.

1. The above example: classic view, arrows between user's tasks, each task resides on the separate line (instance of GanttChart class);

2. Plain view: all user's tasks reside on the same line (instance of PlainGanttChart class)
![Plain View](/plain.png "Plain View")

3. Offset view: user's tasks just slightly shifted down  (instance of OffsetGanttChart class)
![Offset View](/offset.png "Offset View")
