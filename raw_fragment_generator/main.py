from file_stream import FileStream
from settings import Settings
from raw_writer import RawWriter


def main():
    settings = Settings()

    file_streams = []
    for group in settings.read("files").keys():
        group_number = settings.read("groups")[group]
        file_stream = FileStream(settings.read("files")[group])
        file_streams.append((group_number, file_stream))

    raw_filename = settings.read("output", "filename")
    file_output_directory = settings.read("output", "location")
    raw_writer = RawWriter(raw_filename, directory=file_output_directory)

    fragment_size = settings.read("settings", "fragment_size")

    for group, file_stream in file_streams:
        fragment_data = file_stream.read(fragment_size)
        while fragment_data is not None:
            data_to_write = fragment_data + bytes([1 - group]) + bytes([group])
            raw_writer.write(data_to_write)

            # next data
            fragment_data = file_stream.read(fragment_size)


if __name__ == '__main__':
    main()