# directory-encryptor
Encrypt all files inside a single directory, using Python's `pycrypto` package.

## 1. Prepare Directory
Make a directory, and put files to encrypt inside the directory.
**Directory must not contain subdirectories.**

## 2. Install `pycrypto` package
Install python3 `pycrypto` package. <br/>
- Using `pip`
```bash
$ pip3 install pycrypto
```

## 3. Run Encryptor
Choose an encryptor, then run `main.py`.
```bash
$ python3 main.py
```
Information about encryption algorithms can be found at the pycrypto document page: [pycrypto](https://www.dlitz.net/software/pycrypto/api/2.6/)

Input hints:
```bash
$ Directory to encrypt files: /path/to/the/directory/that/contains/files/to/encrypt/
$ Directory to save encrypted files: /path/to/the/directory/to/save/encrypted/files/
$ Input key length: Length of key string to use (in bytes)
$ Input key of length {}: Input key strings to use, leave empty to use random key.
```
Like,
```bash
$ Directory to encrypt files: /home/user/source/
$ Directory to save encrypted files: /home/user/destination/
$ Input key length: 10
$ Input key of length 10: helloworld
```
