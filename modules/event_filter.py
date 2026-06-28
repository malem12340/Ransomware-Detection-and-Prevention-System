import time


class EventFilter:

    def __init__(self):

        # Stores the last processed event
        self.last_events = {}

        # Ignore duplicate events within this time (seconds)
        self.cooldown = 1

    def allow_event(self, event_type, file_path):

        event_key = f"{event_type}:{file_path}"

        current_time = time.time()

        if event_key in self.last_events:

            last_time = self.last_events[event_key]

            if current_time - last_time < self.cooldown:
                return False

        self.last_events[event_key] = current_time

        return True