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

# Train Batch
plain_train_files, plain_validation_files, plain_test_files = distribute_plain_data()
encrypted_train_files, encrypted_validation_files, encrypted_test_files = distribute_encrypted_data()

plain_train_queue = tf.train.string_input_producer(plain_train_files, shuffle=True)
encrypted_train_queue = tf.train.string_input_producer(encrypted_train_files, shuffle=True)

plain_validation_queue = tf.train.string_input_producer(plain_validation_files, shuffle=False)
encrypted_validation_queue = tf.train.string_input_producer(encrypted_validation_files, shuffle=False)

plain_test_queue = tf.train.string_input_producer(plain_test_files, shuffle=False)
encrypted_test_queue = tf.train.string_input_producer(encrypted_test_files, shuffle=False)

plain_train_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
encrypted_train_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)

plain_validation_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
encrypted_validation_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)

plain_test_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
encrypted_test_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)

_, plain_train_value = plain_train_reader.read(plain_train_queue)
_, encrypted_train_value = encrypted_train_reader.read(encrypted_train_queue)

_, plain_validation_value = plain_validation_reader.read(plain_validation_queue)
_, encrypted_validation_value = encrypted_validation_reader.read(encrypted_validation_queue)

_, plain_test_value = plain_test_reader.read(plain_test_queue)
_, encrypted_test_value = encrypted_test_reader.read(encrypted_test_queue)

data_parser = DataParser()

# Train Data
plain_train_fragment = data_parser.set_data(plain_train_value) \
    .decode_as_unit8() \
    .concat([1, 0]) \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
encrypted_train_fragment = data_parser.set_data(encrypted_train_value) \
    .decode_as_unit8() \
    .concat([0, 1]) \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
train_fragments = [plain_train_fragment, encrypted_train_fragment]
train_selection_mask = tf.reshape(tf.multinomial(tf.log([[10., 10.]]), batch_size), [batch_size])
train_batch = tf.gather(train_fragments, train_selection_mask)
train_data, train_labels = tf.split(train_batch, [input_dimension, num_groups], 1)

# Validation Data
plain_validation_fragment = data_parser.set_data(plain_validation_value) \
    .decode_as_unit8() \
    .concat([1, 0]) \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
encrypted_validation_fragment = data_parser.set_data(encrypted_validation_value) \
    .decode_as_unit8() \
    .concat([0, 1]) \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
validation_fragments = [plain_validation_fragment, encrypted_validation_fragment]
validation_selection_mask = tf.reshape(tf.multinomial(tf.log([[10., 10.]]), batch_size), [batch_size])
validation_batch = tf.gather(validation_fragments, validation_selection_mask)
validation_data, validation_labels = tf.split(validation_batch, [input_dimension, num_groups], 1)

# Train Data
plain_test_fragment = data_parser.set_data(plain_test_value) \
    .decode_as_unit8() \
    .concat([1, 0]) \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
encrypted_test_fragment = data_parser.set_data(encrypted_test_value) \
    .decode_as_unit8() \
    .concat([0, 1]) \
    .cast(data_type) \
    .set_shape([record_bytes]) \
    .get_data()
test_fragments = [plain_test_fragment, encrypted_test_fragment]
test_selection_mask = tf.reshape(tf.multinomial(tf.log([[10., 10.]]), batch_size), [batch_size])
test_batch = tf.gather(test_fragments, test_selection_mask)
test_data, test_labels = tf.split(test_batch, [input_dimension, num_groups], 1)
