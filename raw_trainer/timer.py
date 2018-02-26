import time


class Timer:
    def __init__(self):
        self.total_elapsed_time = 0
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        end_time = time.time()
        self.total_elapsed_time += end_time - self.start_time
        self.start_time = None

    def reset(self):
        self.total_elapsed_time = 0
        self.start_time = None
