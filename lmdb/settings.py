import json
import unittest


class Settings:
    settings = None

    def __init__(self):
        if self.settings is None:
            settings_file = open("./settings.json", "r")
            self.settings = json.load(settings_file)
            settings_file.close()

    def read(self, *args):
        result = self.settings
        try:
            for arg in args:
                result = result[arg]
            return result
        except:
            return None


class SettingsTest(unittest.TestCase):
    def setUp(self):
        self.settings = Settings()

    def test_read(self):
        print(self.settings.read("train", "plain"))
