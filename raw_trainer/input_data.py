import tensorflow as tf
from settings import Settings
from distribute_data import distribute_plain_data, distribute_encrypted_data
from data_parser import DataParser


settings = Settings("./settings.json")

input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")

plain_directory = settings.read("data", "plain")
encrypted_directory = settings.read("data", "encrypted")

batch_size = settings.read("hyperparameters", "batch_size")
validation_batch_size = settings.read("test_info", "validation_batch_size")
test_batch_size = settings.read("test_info", "test_batch_size")
data_type = eval(settings.read("hyperparameters", "data_type"))

record_bytes = input_dimension + num_groups

plain_train_files, plain_validation_files, plain_test_files = distribute_plain_data()
encrypted_train_files, encrypted_validation_files, encrypted_test_files = distribute_encrypted_data()

train_files = plain_train_files + encrypted_train_files
validation_files = plain_validation_files + encrypted_validation_files
test_files = plain_test_files + encrypted_test_files

train_queue = tf.train.string_input_producer(train_files, shuffle=True)
validation_queue = tf.train.string_input_producer(validation_files, shuffle=False)
test_queue = tf.train.string_input_producer(test_files, shuffle=False)

train_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
validation_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
test_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)

_, train_value = train_reader.read(train_queue)
_, validation_value = validation_reader.read(validation_queue)
_, test_value = test_reader.read(test_queue)

data_parser = DataParser()

# Train Data
train_fragment = data_parser.set_data(train_value) \
    .decode_as_unit8() \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
train_batch = tf.train.batch([train_fragment], batch_size=batch_size)
train_data, train_labels = tf.split(train_batch, [input_dimension, num_groups], 1)

# Validation Data
validation_fragment = data_parser.set_data(validation_value) \
    .decode_as_unit8() \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
validation_batch = tf.train.batch([validation_fragment], batch_size=validation_batch_size)
validation_data, validation_labels = tf.split(validation_batch, [input_dimension, num_groups], 1)

# Test Data
test_fragment = data_parser.set_data(test_value) \
    .decode_as_unit8() \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
test_batch = tf.train.batch([test_fragment], batch_size=test_batch_size)
test_data, test_labels = tf.split(test_batch, [input_dimension, num_groups], 1)
