import os


class File:
    def __init__(self, filename, directory="./"):
        self.file_path = os.path.join(directory, filename)
        self.file = open(self.file_path, "rb")

    def __del__(self):
        self.file_path = None
        self.file.close()

    def read(self, fragment_size):
        read_data = self.file.read(fragment_size)
        if len(read_data) != fragment_size:
            return None
        return read_data
