import os
import random
from settings import Settings


def distribute_plain_data():
    settings = Settings("./settings.json")

    plain_location = settings.read("data", "plain")
    proportion_train = settings.read("data_info", "proportion", "train")
    proportion_validation = settings.read("data_info", "proportion", "validation")
    proportion_test = settings.read("data_info", "proportion", "test")
    
    raw_filenames = os.listdir(plain_location)
    num_files = len(raw_filenames)
    filenames = list(filter(lambda filename: ("." in filename) and (not filename.startswith(".")), raw_filenames))
    file_paths = list(map(lambda filename: os.path.join(plain_location, filename), filenames))

    random.shuffle(file_paths)
    
    train_index = num_files * proportion_train
    validation_index = train_index + (num_files * proportion_validation)
    test_index = validation_index + (num_files * proportion_test)
    
    return file_paths[0:train_index], file_paths[train_index:validation_index], file_paths[validation_index:test_index]


def distribute_encrypted_data():
    settings = Settings("./settings.json")

    encrypted_location = settings.read("data", "encrypted")
    proportion_train = settings.read("data_info", "proportion", "train")
    proportion_validation = settings.read("data_info", "proportion", "validation")
    proportion_test = settings.read("data_info", "proportion", "test")

    raw_filenames = os.listdir(encrypted_location)
    num_files = len(raw_filenames)
    filenames = list(filter(lambda filename: ("." in filename) and (not filename.startswith(".")), raw_filenames))
    file_paths = list(map(lambda filename: os.path.join(encrypted_location, filename), filenames))

    random.shuffle(file_paths)

    train_index = num_files * proportion_train
    validation_index = train_index + (num_files * proportion_validation)
    test_index = validation_index + (num_files * proportion_test)

    return file_paths[0:train_index], file_paths[train_index:validation_index], file_paths[validation_index:test_index]
