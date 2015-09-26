#!/usr/bin/env python

import json
from datetime import datetime

class Event:
    def __init__(self, occasion, invited_count, year, month, day, cancelled=False):
        self.occasion = occasion
        self.invited_count = invited_count
        self.year = year
        self.month = month
        self.day = day
        self.cancelled = cancelled
        self._date = None

    def __str__(self):
        return "%s: %s (%d invites) %s" % (self.date.strftime("%b %d %Y"),
                                   self.occasion,
                                   self.invited_count,
                                   "[CANCELLED]" if self.cancelled else "")

    @property
    def date(self):
        if self._date is None:
            self._date = datetime(month=self.month, day=self.day, year=self.year)
        return self._date
    
    @date.setter
    def date(self, value):
        self._date = value

def load_json(path):
    """Load JSON data from a file and return list of Event objects."""
    events = []
    try:
        with open(path, 'r') as fd:
            data = fd.read()
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        return []
    except:
        raise

    jsondata = json.loads(data)
    if 'events' not in jsondata:
        return []
    for e in jsondata['events']:
        event = Event(occasion=e['occasion'],
                      invited_count=e['invited_count'],
                      year=e['year'],
                      month=e['month'],
                      day=e['day'],
                      cancelled=e['cancelled'] if 'cancelled' in e else False)
        events.append(event)
    
    return events

def report(events):
    output = []
    past_events = []
    today_events = []
    upcoming_events = []
    today = datetime.today()

    events.sort(key=lambda x: x.date)
    for e in events:
        if e.date < today:
            past_events.append(e)
        elif e.date == today:
            today_events.append(e)
        else:
            upcoming_events.append(e)
    
    if past_events:
        output.append("PAST EVENTS: ")
    for e in past_events:
        output.append("\t%s" % (e))

    output.append("\nTODAY'S EVENTS: ")
    if not today_events:
        output.append("\tYou have no events today.")
    else:
        for e in today_events:
            output.append("\t%s" % (e))
    
    output.append("\nUPCOMING EVENTS: ")
    if not upcoming_events:
        output.append("\tYou have no upcoming events.")
    else:
        for e in upcoming_events:
            output.append("\t%s" % (e))
            
    return output


if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="path to event data",
                        action='store', dest='jsonfile', default='events.txt')
    options = parser.parse_args()
    
    jsonfile = options.jsonfile

    events = load_json(jsonfile)
    if events:
        print '\n'.join(report(events))

    
