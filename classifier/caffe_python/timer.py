import time


class Timer:
    def __init__(self, name):
        self.name = name
        self.elapsed_time = 0
        self.start_time = 0
        self.count = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        end_time = time.time()
        self.elapsed_time += end_time - self.start_time
        self.count += 1

    def print(self):
        print("{}: {} secs ({} on average)".format(self.name,
                                                   self.elapsed_time,
                                                   self.elapsed_time / self.count))
