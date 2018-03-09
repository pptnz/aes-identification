import os


class CSVWriter:
    def __init__(self, filename, directory="./"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_location = os.path.join(directory, filename)
        self.csv_file = open(file_location, "w")

    def __del__(self):
        self.csv_file.close()

    def write(self, data):
        data_in_str = [str(datum) for datum in data]
        data_to_write = ','.join(data_in_str)
        self.csv_file.write("{}\n".format(data_to_write))
