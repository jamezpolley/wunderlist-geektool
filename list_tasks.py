#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" wunderlist-display Looks up the projects and tasks in your wunderlist.db.
Exports them in a ANSI marked up manner appropriate for display in geektool3.
Based on code from Matthew Cave https://github.com/ender3/wunderlist-geektool
"""

import datetime
import getpass
import sqlite3

USERNAME=getpass.getuser()

db_filename = ("/Users/%s/Library/Wunderlist/wunderlist.db" % USERNAME)
conn = sqlite3.connect(db_filename)
conn.row_factory = sqlite3.Row

ESCAPE_IMPORTANT_COLOR = u"\033[33m" # defaults to yellow
ESCAPE_PAST_DUE_COLOR = u"\033[31m" # defaults to red
ESCAPE_PROJECT_NAME_MARKUP = u"\033[1m" # defauls to bold
ESCAPE_NOTE_MARKUP = u"\033[3m" # defaults to italic
ESCAPE_CANCEL = u"\033[0m" # resets all text atributes you may have set
INDENT = u"    "


list_cursor = conn.cursor()
lists = list_cursor.execute("select id, name, position from lists where deleted = '0' order by position")
for list in lists:
    printedHeader = False
    task_cursor = conn.cursor()
    tasks = task_cursor.execute("select id, date, name, note, important, "
            "position from tasks where deleted = 0 and done = 0 and "
            "list_id = ? order by date ASC, important DESC, position",
            str(list["id"]))

    for task in tasks:
        # There is a task associated with this list, so print the header
        if (printedHeader == False):
            print
            print ESCAPE_PROJECT_NAME_MARKUP + list['name'] + ESCAPE_CANCEL
            printedHeader = True

        taskToOutput = []
        # if there is a date, print it before the name of the task
        if (task['date'] != 0 ):
            date = datetime.date.fromtimestamp(task['date'])
            today = datetime.date.today()

            #if the date is in the past, print the date in red
            if (today > date):
                taskToOutput.extend((INDENT, ESCAPE_PAST_DUE_COLOR, 
                    unicode(date.strftime('%x')), ESCAPE_CANCEL, u" - "))
            else:
                taskToOutput.extend((INDENT, unicode(date.strftime('%x')),
                    u" - "))
        else:
            taskToOutput.append(INDENT)

        if (task['important'] == 1):
          taskToOutput.extend((ESCAPE_IMPORTANT_COLOR, u"★ ", ESCAPE_CANCEL))
        taskToOutput.extend((task['name']))

        print ''.join(unicode(x) for x in taskToOutput)

        # if there is a note, print it in italics
        if task['note']:
          print INDENT + INDENT + ESCAPE_NOTE_MARKUP + task['note'] + ESCAPE_CANCEL 
