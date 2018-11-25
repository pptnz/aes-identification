import os
import json
import unittest


def compute_bfd(fragment):
    """
    Compute bfd of a given file fragment.
    :param fragment: file fragment, in bytes type.
    :return: bfd, in python list type of length 256.
    """
    bfd = [0 for _ in range(256)]
    for byte in fragment:
        bfd[int(byte)] += 1

    return bfd


def make_directory(file_path):
    """
    Make a directory for given file_path, if one does not exist.
    For example, if file_path is /path/to/test/file.exe,
    this function creates /path/to/test directory.
    :param file_path: file's path to create containing directory
    """
    directory_path = os.path.dirname(file_path)
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def read_settings(settings_file_path, *args):
    """
    Read json-formatted settings file.
    :param settings_file_path: path to settings.json file
    :param args: key values to read, in string format.
                 for example, to read settings.json[a][b], set *args to "a", "b".
    :return: read settings value from the settings.json file.
    """
    with open(settings_file_path, mode="r") as settings_file:
        settings_json = json.load(settings_file)

    for arg in args:
        settings_json = settings_json[arg]

    return settings_json


def print_progress(current_level, max_level):
    """
    Print current progress to the terminal.
    :param current_level: current progress level
    :param max_level: maximum progress level
    """
    num_bars = int(current_level / max_level * 50)
    num_spaces = 50 - num_bars
    print("|{}>{}| ({}/{}, {:.2f}%)".format("=" * num_bars,
                                           " " * num_spaces,
                                           current_level,
                                           max_level,
                                           current_level / max_level * 100),
          end="\r")


def get_file_size(file_path):
    """
    Return the file size, in bytes.
    :param file_path: path to file to get the size
    :return: file size at file_path, in bytes
    """
    return os.path.getsize(file_path)


class HelperFunctionsTest(unittest.TestCase):
    def test_compute_bfd(self):
        fragment = b"\x00\x01\x02\x03\x01\x02\x03\x02\x03\x03"
        bfd = compute_bfd(fragment)

        self.assertEqual(bfd[0], 1)
        self.assertEqual(bfd[1], 2)
        self.assertEqual(bfd[2], 3)
        self.assertEqual(bfd[3], 4)
        for i in range(4, len(bfd)):
            self.assertEqual(bfd[i], 0)

    def test_make_directory(self):
        make_directory("./test/test/test.test")

        self.assertTrue(os.path.exists("./test"))
        self.assertTrue(os.path.exists("./test/test"))

        os.removedirs("./test/test")

    def test_read_settings(self):
        with open("./test_settings.json", "w") as file:
            file.write("{\"a\": {\"b\": 3}}")

        self.assertEqual(read_settings("./test_settings.json", "a", "b"), 3)

        os.remove("./test_settings.json")

    def test_get_file_size(self):
        with open("./test_file_size.test", "wb") as file:
            file.write(b"\x00\x00\x00\x00\x00")

        self.assertEqual(get_file_size("./test_file_size.test"), 5)

        os.remove("./test_file_size.test")
