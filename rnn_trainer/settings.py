import json


class Settings:
    settings_json = None

    def __init__(self, settings_file_location):
        if Settings.settings_json is None:
            with open(settings_file_location, "r") as settings_file:
                Settings.settings_json = json.load(settings_file)

    @staticmethod
    def read(*args):
        read_setting = Settings.settings_json
        for arg in args:
            read_setting = read_setting[arg]
        return read_setting
