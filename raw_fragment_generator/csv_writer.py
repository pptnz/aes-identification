import os


class CSVWriter:
    def __init__(self, num_lines_per_csv, filename, directory="./"):
        self.csv_file_count = 1
        self.num_lines_per_csv = num_lines_per_csv
        self.file_location = os.path.join(directory, filename)
        self.data_buffer = []

        if not os.path.exists(directory):
            os.makedirs(directory)

    def write(self, data_list):
        self.data_buffer.append(data_list)
        if len(self.data_buffer) >= self.num_lines_per_csv:
            for i in range(len(self.data_buffer)):
                self.data_buffer[i] = ','.join(str(data) for data in self.data_buffer[i])
            with open(self.file_location.format(self.csv_file_count), "w") as csv_file:
                data_to_write = '\n'.join(row for row in self.data_buffer)
                csv_file.write(data_to_write)
            self.data_buffer = []
            self.csv_file_count += 1
