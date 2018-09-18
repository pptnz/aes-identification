from file import File
from print_progress import print_progress
import os
import random
import string


def main():
    choice = int(input("0-Encrypt, 1-Decrypt: "))
    if choice == 0:
        directory = input("Directory to encrypt files: ")
        output_directory = input("Directory to save encrypted files: ")
        key_length = int(input("Input key length: "))
        if key_length <= 0:
            print("Wrong key length!")
            exit(-1)
        key = input("Input key of length {} (leave empty to use random key for each file): ".format(key_length))
        if len(key) != 0 and len(key) != key_length:
            print("Wrong key size!")
            exit(-1)

        num_files = 0
        for _, _, file_names in os.walk(directory):
            num_files += len(list(filter(lambda filename: not filename.startswith("."), file_names)))

        files_count = 1

        if len(key) == key_length:
            for directory_path, directory_names, file_names in os.walk(directory):
                # Compute Destination Directory
                destination_directory = directory_path.replace(directory, output_directory)
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)

                # Work with files
                for file_name in file_names:
                    if file_name.startswith("."):
                        continue

                    file = File(file_name, directory=directory_path)
                    file.encrypt(key, file_name + ".encrypted", directory=destination_directory)
                    print_progress(files_count, num_files)
                    files_count += 1

        else:
            for directory_path, directory_names, file_names in os.walk(directory):
                # Compute Destination Directory
                destination_directory = directory_path.replace(directory, output_directory)
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)

                # Work with files
                for file_name in file_names:
                    if file_name.startswith("."):
                        continue

                    file = File(file_name, directory=directory_path)
                    key = ""
                    for _ in range(key_length):
                        key += random.choice(string.ascii_letters + string.digits + string.punctuation)
                    file.encrypt(key, file_name + ".encrypted", directory=destination_directory)
                    print_progress(files_count, num_files)
                    files_count += 1

    elif choice == 1:
        directory = input("Directory to decrypt files: ")
        output_directory = input("Directory to save decrypted files: ")
        key_length = int(input("Input key length: "))
        if key_length <= 0:
            print("Wrong key length!")
            exit(-1)
        key = input("Input key of length {}: ".format(key_length))
        if len(key) != key_length:
            print("Wrong key size!")
            exit(-1)

        num_files = 0
        for _, _, file_names in os.walk(directory):
            num_files += len(list(filter(lambda filename: not filename.startswith("."), file_names)))

        files_count = 1

        for directory_path, directory_names, file_names in os.walk(directory):
            # Compute Destination Directory
            destination_directory = directory_path.replace(directory, output_directory)
            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)

            # Work with files
            for file_name in file_names:
                if file_name.startswith("."):
                    continue

                file = File(file_name, directory=directory_path)
                file.decrypt(key, file_name.replace(".encrypted", ""), directory=destination_directory)
                print_progress(files_count, num_files)
                files_count += 1


if __name__ == '__main__':
    main()
