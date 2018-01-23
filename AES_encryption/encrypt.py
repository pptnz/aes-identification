# Reference
# encrypt, decrypt from https://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto
# pad, unpad from https://gist.github.com/dokenzy/7b64238424175742a8a1

from Crypto.Cipher import AES
from Crypto import Random

BLOCK_SIZE = 16
initial_vector = BLOCK_SIZE * '\x00'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE).encode()
unpad = lambda s: s[:-ord(s[len(s)-1:])]


def encrypt(key, plaintext):
    encryptor = AES.new(key, AES.MODE_CBC, initial_vector)

    ciphertext = encryptor.encrypt(pad(plaintext))
    return ciphertext


def decrypt(key, ciphertext):
    decryptor = AES.new(key, AES.MODE_CBC, initial_vector)

    plaintext = unpad(decryptor.decrypt(ciphertext))
    return plaintext


# 32 Byte key
key = b'hello, world! Nice to meet you:)'
plaintext = "안녕"
ciphertext = encrypt(key, plaintext.encode())

print(ciphertext)

plaintext = decrypt(key, ciphertext).decode()
print(plaintext)

with open(location, "wb") as result:
    with open(location, "rb") as file:
        data_to_encrypt = file.read(16)
        while len(data_to_encrypted) == 16:


        data_encrypted = encrypt(data_to_encrypt)
            result.write(data_encrypted)

