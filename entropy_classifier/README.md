# Entropy Classifier
This C++ program classifies whether file fragments are encrypted or not, using histogram and entropy based methods.

# How to Use
## 1. Prepare `Makefile` using `cmake`
To compile the project, generate `Makefile` using `cmake`.
```bash
$ cmake .
```

## 2. Compile project
Compile the project using makefile.
```bash
$ make
```

## 3. Change Settings
Change settings at `settings.txt` file.
```
line 1: /path/to/directory/that/contains/plain/files/            <- Trailing separator is mandatory. Directory must exist!
line 2: /path/to/directory/that/contains/encrypted/files/        <- Trailing separator is mandatory. Directory must exist!!
line 3: Number of plain fragments to test. 0 not to test, -1 to test as much as possible.
line 4: Number of encrypted fragments to test. 0 not to test, -1 to test as much as possible.
line 5: Size of fragment in bytes
```

For example,
```
/home/user/data/plain/
/home/user/data/encrypted
10000
-1
4096
```

## 4. Run Program
Run the program and see the result.
```bash
$ ./entropy_classifier
```
