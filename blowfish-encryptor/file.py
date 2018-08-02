from encryptor import Encryptor
import os


class File:
    def __init__(self, filename, directory="./"):
        self.file_location = os.path.join(directory, filename)

    def encrypt(self, key, filename, directory="./"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        destination = os.path.join(directory, filename)

        try:
            with open(destination, "wb") as destination_file:
                with open(self.file_location, "rb") as original_file:
                    plain_text = original_file.read()
                    cipher_text = Encryptor.encrypt(key, plain_text)
                    destination_file.write(cipher_text)

            # self.file_location = destination
        except OSError:
            pass

    def decrypt(self, key, filename, directory="./"):
        if not os.path.exists(directory):
            os.makedirs(directory)
        destination = os.path.join(directory, filename)

        with open(destination, "wb") as destination_file:
            with open(self.file_location, "rb") as original_file:
                cipher_text = original_file.read()
                plain_text = Encryptor.decrypt(key, cipher_text)
                destination_file.write(plain_text)

        # self.file_location = destination

