import random
from file_stream import FileStream
from settings import Settings
from csv_writer import CSVWriter
from summary import summary


def main():
    settings = Settings()

    file_streams = []
    for group in settings.read("files").keys():
        group_number = settings.read("groups")[group]
        file_stream = FileStream(settings.read("files")[group])
        file_streams.append((group_number, file_stream))

    num_groups = len(file_streams)
    fragments_per_csv = settings.read("output", "fragments_per_csv")
    csv_filename = settings.read("output", "filename")
    csv_output_directory = settings.read("output", "location")
    csv_writer = CSVWriter(fragments_per_csv, csv_filename, directory=csv_output_directory)

    fragment_size = settings.read("settings", "fragment_size")
    random_generation_turned_on = settings.read("settings", "random")

    if random_generation_turned_on:
        while len(file_streams) != 0:
            group, file_stream = random.choice(file_streams)
            fragment_data = file_stream.read(fragment_size)

            if fragment_data is None:
                # file stream is exhausted.
                file_streams.remove((group, file_stream))
                continue

            data_summarized = summary(fragment_data, fragment_size)
            one_hot_encoding = [0 for _ in range(num_groups)]
            one_hot_encoding[group] = 1
            data_to_write = data_summarized + one_hot_encoding
            csv_writer.write(data_to_write)
    else:
        for group, file_stream in file_streams:
            fragment_data = file_stream.read(fragment_size)
            while fragment_data is not None:
                data_summarized = summary(fragment_data, fragment_size)
                one_hot_encoding = [0 for _ in range(num_groups)]
                one_hot_encoding[group] = 1
                data_to_write = data_summarized + one_hot_encoding
                csv_writer.write(data_to_write)

                # next data
                fragment_data = file_stream.read(fragment_size)


if __name__ == '__main__':
    main()