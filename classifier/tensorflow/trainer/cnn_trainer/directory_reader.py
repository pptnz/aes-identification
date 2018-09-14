import tensorflow as tf
import os


class DirectoryReader:
    def __init__(self, directory, record_bytes, shuffle=False):
        file_names = list(
            filter(lambda filename: ("." in filename) and (not filename.startswith(".")), os.listdir(directory)))
        file_urls = list(map(lambda filename: os.path.join(directory, filename), file_names))

        self.file_queue = tf.train.string_input_producer(file_urls, shuffle=shuffle)
        self.file_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)

    def read(self):
        _, read_value = self.file_reader.read(self.file_queue)
        return read_value
