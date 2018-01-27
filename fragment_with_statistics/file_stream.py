import os
from file import File


class FileStream:
    def __init__(self, directory="./"):
        self.directory = directory
        self.filename_queue = list(filter(lambda filename: (not filename.startswith(".")) and ("." in filename),
                                          os.listdir(directory)))
        self.file = None
        self.set_to_next_file()

    def set_to_next_file(self):
        if len(self.filename_queue) == 0:
            self.file = None
            return False

        self.file = File(self.filename_queue.pop(), self.directory)
        return True

    def read(self, fragment_size):
        read_data = self.file.read(fragment_size)
        while read_data is None:
            change_succeeded = self.set_to_next_file()
            if not change_succeeded:
                return None
            read_data = self.file.read(fragment_size)
        return read_data
