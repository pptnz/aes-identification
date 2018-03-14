import os
from file import File
from print_progress import print_progress


class FileStream:
    total_files_count = 0
    current_files_count = 0

    def __init__(self, directory="./", destructive=False):
        self.directory = directory
        self.destructive = destructive
        self.filename_queue = list(filter(lambda filename: (not filename.startswith(".")) and ("." in filename),
                                          os.listdir(directory)))
        FileStream.total_files_count += len(self.filename_queue)
        self.file = None
        self.set_to_next_file()

    def set_to_next_file(self):
        if self.destructive:
            os.remove(self.file.file_path)

        if len(self.filename_queue) == 0:
            self.file = None
            return False

        self.file = File(self.filename_queue.pop(), self.directory)

        FileStream.current_files_count += 1
        print_progress(FileStream.current_files_count, FileStream.total_files_count)

        return True

    def read(self, fragment_size):
        read_data = self.file.read(fragment_size)
        while read_data is None:
            change_succeeded = self.set_to_next_file()
            if not change_succeeded:
                return None
            read_data = self.file.read(fragment_size)
        return read_data
