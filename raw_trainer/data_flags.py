class DataFlags:
    data = {}

    @staticmethod
    def put(key, data):
        DataFlags.data[key] = data

    @staticmethod
    def get(key):
        return DataFlags.data[key]
