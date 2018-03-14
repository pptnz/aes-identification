class DataFlags:
    data = {}

    @staticmethod
    def put(key, data):
        DataFlags.data[key] = data

    @staticmethod
    def get(key):
        return DataFlags.data[key]

    @staticmethod
    def add(key, value):
        if key not in DataFlags:
            DataFlags[key] = 0
        DataFlags.data[key] += value

