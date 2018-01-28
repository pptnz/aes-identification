def main():
    log_file_path = input("Log File: ")

    with open(log_file_path, "r") as log_file:
        with open("./result.log", "w") as result_file:
            for line in log_file.readlines():
                if not line.strip().startswith("|"):
                    result_file.write(line)


if __name__ == '__main__':
    main()