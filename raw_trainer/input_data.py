import tensorflow as tf
from settings import Settings
from directory_reader import DirectoryReader
from data_parser import DataParser

settings = Settings("./settings.json")

input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")

train_plain_directory = settings.read("train_data", "plain")
train_encrypted_directory = settings.read("train_data", "encrypted")

validation_file_location = settings.read("validation_data", "location")
validation_file_begin = settings.read("validation_data", "begin")
validation_file_end = settings.read("validation_data", "end")

test_file_location = settings.read("test_data", "location")
test_file_begin = settings.read("test_data", "begin")
test_file_end = settings.read("test_data", "end")

batch_size = settings.read("hyperparameters", "batch_size")
validation_batch_size = settings.read("test_info", "validation_batch_size")
test_batch_size = settings.read("test_info", "test_batch_size")

record_bytes = input_dimension + num_groups

# Train Batch
train_plain_reader = DirectoryReader(train_plain_directory, input_dimension, shuffle=True)
train_encrypted_reader = DirectoryReader(train_encrypted_directory, input_dimension, shuffle=True)

train_plain_value = train_plain_reader.read()
train_encrypted_value = train_encrypted_reader.read()

data_parser = DataParser()

train_plain_fragment = data_parser.set_data(train_plain_value) \
    .decode_as_unit8() \
    .concat([1, 0]) \
    .cast(tf.float32) \
    .set_shape([record_bytes]) \
    .get_data()
train_encrypted_fragment = data_parser.set_data(train_encrypted_value) \
    .decode_as_unit8() \
    .concat([0, 1]) \
    .cast(tf.float32) \
    .set_shape([record_bytes]) \
    .get_data()

train_fragments = [train_plain_fragment, train_encrypted_fragment]
train_selection_mask = tf.reshape(tf.multinomial(tf.log([[10., 10.]]), batch_size), [batch_size])
train_batch = tf.gather(train_fragments, train_selection_mask)
train_data, train_labels = tf.split(train_batch, [input_dimension, num_groups], 1)

# Validation Batch
validation_files = [validation_file_location.format(i) for i in range(validation_file_begin, validation_file_end + 1)]
validation_queue = tf.train.string_input_producer(validation_files, shuffle=False)
validation_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
_, validation_value = validation_reader.read(validation_queue)
validation_fragment = tf.cast(tf.decode_raw(validation_value, tf.uint8), tf.float32)
validation_fragment.set_shape([record_bytes])
validation_batch = tf.train.batch([validation_fragment], batch_size=validation_batch_size)
validation_data, validation_labels = tf.split(validation_batch, [input_dimension, num_groups], 1)

# Test Batch
test_files = [test_file_location.format(i) for i in range(test_file_begin, test_file_end + 1)]
test_queue = tf.train.string_input_producer(test_files, shuffle=False)
test_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
_, test_value = test_reader.read(test_queue)
test_fragment = tf.cast(tf.decode_raw(test_value, tf.uint8), tf.float32)
test_fragment.set_shape([record_bytes])
test_batch = tf.train.batch([test_fragment], batch_size=test_batch_size)
test_data, test_labels = tf.split(test_batch, [input_dimension, num_groups], 1)
