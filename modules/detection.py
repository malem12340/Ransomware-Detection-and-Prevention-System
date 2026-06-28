import time
from collections import deque


class DetectionEngine:

    def __init__(self):

        self.events = deque()

        self.THRESHOLD = 20      # Number of events

        self.TIME_WINDOW = 10    # Seconds

    def check(self):

        current_time = time.time()

        self.events.append(current_time)

        while self.events and current_time - self.events[0] > self.TIME_WINDOW:

            self.events.popleft()

        if len(self.events) >= self.THRESHOLD:

            return True

        return False