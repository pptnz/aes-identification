import os
import random


def main():
    input_directory = input("Input Directory: ")
    train_destination = input("Train file destination: ")
    validation_destination = input("Validation file destination: ")
    test_destination = input("Test file destination: ")
    train_percentage = int(input("Train file in %: "))
    test_percentate = int(input("Test file in %: "))
    test_percentate += train_percentage
    
    if not os.path.exists(train_destination):
        os.makedirs(train_destination)
        
    if not os.path.exists(validation_destination):
        os.makedirs(validation_destination)

    if not os.path.exists(test_destination):
        os.makedirs(test_destination)

    files = list(filter(lambda filename: (not filename.startswith(".")) and ("." in filename),
                        os.listdir(input_directory)))

    for filename in files:
        file_path = os.path.join(input_directory, filename)

        random_result = random.randrange(0, 100)
        if random_result < train_percentage:
            os.rename(file_path, os.path.join(train_destination, filename))
        elif random_result < test_percentate:
            os.rename(file_path, os.path.join(test_destination, filename))
        else:
            os.rename(file_path, os.path.join(validation_destination, filename))


if __name__ == '__main__':
    main()
