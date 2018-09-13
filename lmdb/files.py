import os
import unittest


class FileExhaustedError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Files:
    def __init__(self, path):
        self.file_names = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        self.file_index = 0
        self.path = path
        first_file = os.path.join(self.path, self.file_names[self.file_index])
        self.file = open(first_file, "rb")

    def set_to_next_file(self):
        self.file_index += 1
        if self.file_index >= len(self.file_names):
            # all files exhausted
            raise FileExhaustedError("files at path '{}' exhausted.".format(self.path))
        file_path = os.path.join(self.path, self.file_names[self.file_index])
        self.file.close()
        self.file = open(file_path, "rb")

    def read(self, size):
        data = self.file.read(size)
        while len(data) < size:
            # short count
            self.set_to_next_file()
            data = self.file.read(size)
        return data


class FilesTest(unittest.TestCase):
    def setUp(self):
        self.files = Files(path="./")

    def test_read(self):
        for _ in range(100):
            try:
                print(self.files.read(size=50))
            except FileExhaustedError:
                return
