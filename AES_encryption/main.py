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
        key = input("Input key of length 32 (leave empty to use random key for each file): ")
        if len(key) != 0 and len(key) != 32:
            print("Wrong key size for AES-256!")
            exit(-1)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        num_files = len(os.listdir(directory))
        files_count = 1

        if len(key) == 32:
            for filename in os.listdir(directory):
                if filename.startswith("."):
                    continue
                file = File(filename, directory=directory)
                file.encrypt(key, filename + ".encrypted", directory=output_directory)
                print_progress(files_count, num_files)
                files_count += 1

        else:
            for filename in os.listdir(directory):
                if filename.startswith("."):
                    continue
                file = File(filename, directory=directory)
                key = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=32))
                file.encrypt(key, filename + ".encrypted", directory=output_directory)
                print_progress(files_count, num_files)
                files_count += 1

    elif choice == 1:
        directory = input("Directory to decrypt files: ")
        output_directory = input("Directory to save decrypted files: ")
        key = input("Input key of length 32: ")
        if len(key) != 32:
            print("Wrong key size for AES-256!")
            exit(-1)

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        num_files = len(os.listdir(directory))
        files_count = 1

        for filename in os.listdir(directory):
            if filename.startswith("."):
                continue
            file = File(filename, directory=directory)
            file.decrypt(key, filename.replace(".encrypted", ""), directory=output_directory)
            print_progress(files_count, num_files)
            files_count += 1


if __name__ == '__main__':
    main()