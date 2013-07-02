ganttchart
==========

This library allows to create simple gantt-charts like the one below.
![Gantt chart generated](/out.png "Gantt chart generated")

[local.py](/local.py) demonstrates sample usage with [test.csv](/test.csv) file as a data source.
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
