from aes_encryptor import AESEncryptor
import os


class File:
    def __init__(self, filename, directory="./"):
        self.file_location = os.path.join(directory, filename)

    def encrypt(self, key, filename, directory="./"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        destination = os.path.join(directory, filename)

        with open(destination, "wb") as destination_file:
            with open(self.file_location, "rb") as original_file:
                plain_text = original_file.read()
                cipher_text = AESEncryptor.encrypt(key, plain_text)
                destination_file.write(cipher_text)

        self.file_location = destination

    def decrypt(self, key, filename, directory="./"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        destination = os.path.join(directory, filename)

        with open(destination, "wb") as destination_file:
            with open(self.file_location, "rb") as original_file:
                cipher_text = original_file.read()
                plain_text = AESEncryptor.decrypt(key, cipher_text)
                destination_file.write(plain_text)

        self.file_location = destination

    def split_file(self, fragment_size, filename_format, start_number, directory="./"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        destination_format = os.path.join(directory, filename_format)
        file_number = start_number

        with open(self.file_location, "rb") as original_file:
            fragment = original_file.read(fragment_size)
            while len(fragment) == fragment_size:
                with open(destination_format.format(file_number), "wb") as destination_file:
                    destination_file.write(fragment)

                file_number += 1
                fragment = original_file.read(fragment_size)

        return file_number
