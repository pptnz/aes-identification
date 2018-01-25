# Reference
# encrypt, decrypt from https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
# pad, unpad from https://gist.github.com/dokenzy/7b64238424175742a8a1

from Crypto.Cipher import AES


class AESEncryptor:
    block_size = 16
    initial_vector = block_size * '\x00'

    @staticmethod
    def pad(plain_text):
        padding_length = AESEncryptor.block_size - (len(plain_text) % AESEncryptor.block_size)
        padding = padding_length * chr(padding_length)
        padding_message = padding.encode()
        return plain_text + padding_message
    
    @staticmethod
    def unpad(plain_text):
        num_padding = ord(plain_text[-1:])
        return plain_text[:-num_padding]

    @staticmethod
    def encrypt(key, plain_text):
        encryptor = AES.new(key, AES.MODE_CBC, AESEncryptor.initial_vector)
        cipher_text = encryptor.encrypt(AESEncryptor.pad(plain_text))
        return cipher_text

    @staticmethod
    def decrypt(key, cipher_text):
        decryptor = AES.new(key, AES.MODE_CBC, AESEncryptor.initial_vector)
        plain_text = AESEncryptor.unpad(decryptor.decrypt(cipher_text))
        return plain_text
