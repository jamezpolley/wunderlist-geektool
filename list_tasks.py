#!/usr/bin/env python
""" wunderlist-display Looks up the projects and tasks in your wunderlist.db.
Exports them in a ANSI marked up manner appropriate for display in geektool3.
Based on code from Matthew Cave https://github.com/ender3/wunderlist-geektool
"""

import datetime
import sqlite3

USERNAME="james"

conn = sqlite3.connect("/Users/%s/Library/Application Support/Titanium/"
        "appdata/com.wunderkinder.wunderlist/wunderlist.db" % USERNAME)
conn.row_factory = sqlite3.Row

ESCAPE_IMPORTANT_COLOR = "\033[33m" # defaults to yellow
ESCAPE_PAST_DUE_COLOR = "\033[31m" # defaults to red
ESCAPE_PROJECT_NAME_MARKUP = "\033[1m" # defauls to bold
ESCAPE_NOTE_MARKUP = "\033[3m" # defaults to italic
ESCAPE_CANCEL = "\033[0m" # resets all text atributes you may have set
INDENT = "    "


list_cursor = conn.cursor()
lists = cursor.execute("select id, name, position from lists where deleted = '0' order by position")
for list in lists:
    printedHeader = False
    task_cursor = conn.cursor()
    tasks = task_cursor.execute("select id, date, name, note, important, "
            "position from tasks where deleted = 0 and done = 0 and "
            "list_id = ? order by date DESC, important DESC, position",
            list["id"])

    for task in tasks:
        # There is a task associated with this list, so print the header
        if (printedHeader == False):
            print
            print ESCAPE_PROJECT_NAME_MARKUP + list['name'] + ESCAPE_CANCEL
            printedHeader = True

        taskToOutput = []
        # if there is a date, print it before the name of the task
        if (task['date'] != 0 ):
            date = datetime.date(task['date'])
            today = datetime.date(datetime.date.today())

            #if the date is in the past, print the date in red
            if (today > date):
                taskToOutput.append(INDENT + ESCAPE_PAST_DUE_COLOR)
                taskToOutput.append(date.month + "/" + date.day + "/")
                taskToOutput.append(date.year + ESCAPE_CANCEL + " - ")
            else:
                taskToOutput.append(INDENT + date.month + "/" + date.day)
                taskToOutput.append("/" + date.year.to_s + " - ")
        else:
            taskToOutput.append(INDENT)

        if (task['important'] == 1):
          taskToOutput.append(ESCAPE_IMPORTANT_COLOR + "★ " + ESCAPE_CANCEL)
        taskToOutput.append(task['name'])

        print ''.join(taskToOutput)

        # if there is a note, print it in italics
        if task['note']:
          print INDENT + INDENT + ESCAPE_NOTE_MARKUP + task['note'] + ESCAPE_CANCEL 
