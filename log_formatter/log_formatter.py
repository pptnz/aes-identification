import os


def main():
    log_filename_queue = list(filter(lambda filename: filename.endswith(".log"), os.listdir("./")))

    for log_filename in log_filename_queue:
        new_log_file_path = os.path.join("./", log_filename)
        orig_log_file_path = new_log_file_path + ".orig"
        os.rename(new_log_file_path, orig_log_file_path)
        with open(orig_log_file_path, "r") as log_file:
            with open(new_log_file_path, "w") as result_file:
                for line in log_file.readlines():
                    if not line.strip().startswith("|"):
                        result_file.write(line)


if __name__ == '__main__':
    main()