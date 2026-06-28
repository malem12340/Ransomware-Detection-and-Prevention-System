from modules.event_filter import EventFilter
import time

event_filter = EventFilter()

print(event_filter.allow_event("Created", "test.txt"))

print(event_filter.allow_event("Created", "test.txt"))

time.sleep(2)

print(event_filter.allow_event("Created", "test.txt"))