python-ted
==========

Python library for the University of Edinburgh's [T@Ed Timetabling Service][ted].

**Disclaimer: This library has not been condoned by the University of Edinburgh.**

`python-ted` is built by students, and simply scrapes the existing timetable web service,
since no APIs or timetabling data have been released by the university.


## Installation

```sh
pip install python-ted
```

### Requires

- [`icalendar`][icalendar]
- [`lxml`](http://lxml.de/)
- [`requests`](https://pypi.python.org/pypi/requests)


## Usage

```python
>>> import icalendar
>>> import ted

# Initialise client and download course-list
>>> timetable = ted.Client()

# Regex match against course list:
>>> import re
>>> timetable.match(re.compile('Data'))
[<Course: INFR08015 (Informatics 1 - Data and Analysis)>, <Course: ...>, ...]
>>> timetable.match(re.compile('INFR08015'))
[<Course: INFR08015 (Informatics 1 - Data and Analysis)>]

# Get a specific course by course-code
>>> timetable.course(code='INFR08015')
<Course: INFR08015 (Informatics 1 - Data and Analysis)>
>>> timetable.course(code='invalid course code')
None
```

Each `Course` object has 3 main attributes:

- `title`: human-readable course name.
- `code`: University of Edinburgh course code (seen on timetables or exam scripts).
- `identifier`: T@Ed-specific course identifier.


```python
>>> course = timetable.course(code='INFR08015')

# Scrape T@Ed for list of weekly course events, and build an ical calendar
>>> events = timetable.events(course)
>>> cal = timetable.calendar(events)

# Render calendar to a bytestring
>>> cal.to_ical()
"BEGIN:VCALENDAR..."
```


Future
------

- Get API access for T@Ed.


License
-------

This Source Code is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.


[ted]: https://www.ted.is.ed.ac.uk/UOE1314_SWS/
[icalendar]: https://pypi.python.org/pypi/icalendar
