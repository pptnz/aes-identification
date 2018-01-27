import json


class Settings:
    settings_json = None

    def __init__(self):
        if Settings.settings_json is None:
            with open("./settings.json", "r") as settings_file:
                Settings.settings_json = json.load(settings_file)

    @staticmethod
    def read(*args):
        settings_read = Settings.settings_json
        for arg in args:
            settings_read = settings_read[arg]
        return settings_read
