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

- [`requests`](https://pypi.python.org/pypi/requests)
- [`icalendar`][icalendar]


## Usage


```python
>>> import icalendar
>>> from ted import TimetablingAtEd


# Initialise client and download course-list
>>> timetable = TimetablingAtEd()


# Search course-list for a substring match
>>> timetable.search('Data')
[<Course: INFR08015 (Informatics 1 - Data and Analysis)>, <Course: ...>, ...]
>>> timetable.search('INFR08015')
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
>>> events = course.events()
>>> cal = icalendar.Calendar()
>>> for e in events:
>>>     cal.add_component(e)

# Shortcut for the above
>>> cal = course.calendar()

# Render calendar to a string
>>> cal.to_ical()
"BEGIN:VCALENDAR..."
```


Future
------

- Support Python 3, once [`icalendar`][icalendar] does.
- Get API access for T@Ed.


License
-------

This Source Code is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.


[ted]: https://www.ted.is.ed.ac.uk/UOE1314_SWS/
[icalendar]: https://pypi.python.org/pypi/icalendar
