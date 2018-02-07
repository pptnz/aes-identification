import os


class RawWriter:
    def __init__(self, filename, directory="./"):
        self.file_count = 1
        self.file_location = os.path.join(directory, filename)

        if not os.path.exists(directory):
            os.makedirs(directory)

    def write(self, raw_data):
        with open(self.file_location.format(self.file_count), "wb") as file:
            file.write(raw_data)
        self.file_count += 1
