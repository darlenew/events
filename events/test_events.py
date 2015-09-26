#!/usr/bin/env python
from events import Event, load_json, report
from datetime import datetime

import unittest
class TestEvent(unittest.TestCase):
    SAMPLE_DATA = 'events.txt'

    def test_event(self):
        e = Event(occasion="World Series",
                  invited_count=80000,
                  year=2016,
                  month=10,
                  day=7)
        self.assertTrue(e.date, datetime(year=2016, month=10, day=7))
        self.assertFalse(e.cancelled)

    def test_load_json(self):
        events = load_json(self.SAMPLE_DATA)
        self.assertEqual(len(events), 4)

if __name__ == "__main__":
    unittest.main()

                        
