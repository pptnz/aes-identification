import os


class File:
    def __init__(self, filename, directory="./"):
        file_path = os.path.join(directory, filename)
        self.file = open(file_path, "rb")

    def __del__(self):
        self.file.close()

    def read(self, fragment_size):
        read_data = self.file.read(fragment_size)
        if len(read_data) != fragment_size:
            return None
        return read_data
