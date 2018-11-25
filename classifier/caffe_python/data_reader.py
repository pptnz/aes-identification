import unittest


class DataReader:
    """
    Opens a file, and reads the file in the form of byte fragments, sequentially.
    """

    def __init__(self, path, read_size=4096):
        """
        Initialize `DataReader` instance.
        :param path: path to the file to read
        :param read_size: file fragment size, in bytes.
        """
        self.input_file = open(path, mode="rb")
        self.read_size = read_size

    def __del__(self):
        """
        Deinitialize the object by closing the file.
        """
        self.input_file.close()

    def read(self):
        """
        Read the file, in byte fragments form.
        :return: file fragment in bytes form.
                 the size of file fragment is `read_size` bytes.
                 if fragment of `read_size` is not available (like short counts), then `None` is returned.
        """
        read_data = self.input_file.read(self.read_size)

        if len(read_data) < self.read_size:
            return None

        return read_data


class DataReaderTest(unittest.TestCase):
    def setUp(self):
        self.read_size = 16
        self.data_reader = DataReader(path="./data_reader.py", read_size=self.read_size)

    def test_read(self):
        data = self.data_reader.read()

        while data is not None:
            self.assertEqual(len(data), self.read_size)

            data = self.data_reader.read()

    def test_deinit(self):
        del self.data_reader
