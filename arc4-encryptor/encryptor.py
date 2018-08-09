# Reference
# encrypt, decrypt from https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
# pad, unpad from https://gist.github.com/dokenzy/7b64238424175742a8a1

from Crypto.Cipher import ARC4


class Encryptor:
    @staticmethod
    def encrypt(key, plain_text):
        encryptor = ARC4.new(key)
        cipher_text = encryptor.encrypt(plain_text)
        return cipher_text

    @staticmethod
    def decrypt(key, cipher_text):
        decryptor = ARC4.new(key)
        plain_text = decryptor.decrypt(cipher_text)
        return plain_text
