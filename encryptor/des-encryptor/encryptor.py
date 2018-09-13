# Reference
# encrypt, decrypt from https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
# pad, unpad from https://gist.github.com/dokenzy/7b64238424175742a8a1

from Crypto.Cipher import DES


class Encryptor:
    block_size = DES.block_size
    initial_vector = b'\x00' * block_size

    @staticmethod
    def pad(plain_text):
        padding_length = Encryptor.block_size - (len(plain_text) % Encryptor.block_size)
        padding = padding_length * chr(padding_length)
        padding_message = padding.encode()
        return plain_text + padding_message
    
    @staticmethod
    def unpad(plain_text):
        num_padding = ord(plain_text[-1:])
        return plain_text[:-num_padding]

    @staticmethod
    def encrypt(key, plain_text):
        encryptor = DES.new(key, DES.MODE_CBC, Encryptor.initial_vector)
        cipher_text = encryptor.encrypt(Encryptor.pad(plain_text))
        return cipher_text

    @staticmethod
    def decrypt(key, cipher_text):
        decryptor = DES.new(key, DES.MODE_CBC, Encryptor.initial_vector)
        plain_text = Encryptor.unpad(decryptor.decrypt(cipher_text))
        return plain_text
