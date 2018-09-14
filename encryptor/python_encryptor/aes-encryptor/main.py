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

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        files = list(filter(lambda filename: (not filename.startswith(".")) and ("." in filename),
                            os.listdir(directory)))
        num_files = len(files)
        files_count = 1

        if len(key) == key_length:
            for filename in files:
                file = File(filename, directory=directory)
                file.encrypt(key, filename + ".encrypted", directory=output_directory)
                print_progress(files_count, num_files)
                files_count += 1

        else:
            for filename in files:
                file = File(filename, directory=directory)
                key = ""
                for _ in range(key_length):
                    key += random.choice(string.ascii_letters + string.digits + string.punctuation)
                file.encrypt(key, filename + ".encrypted", directory=output_directory)
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

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        files = list(filter(lambda filename: (not filename.startswith(".")) and ("." in filename),
                            os.listdir(directory)))
        num_files = len(files)
        files_count = 1

        for filename in files:
            if filename.startswith("."):
                continue
            file = File(filename, directory=directory)
            file.decrypt(key, filename.replace(".encrypted", ""), directory=output_directory)
            print_progress(files_count, num_files)
            files_count += 1


if __name__ == '__main__':
    main()
