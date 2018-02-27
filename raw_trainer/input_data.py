import tensorflow as tf
from settings import Settings

settings = Settings("./settings.json")

train_plain_directory = settings.read("train_data", "plain")
train_encrypted_directory = settings.read("train_data", "encrypted")

train_plain_reader = DirectoryReader("/Users/barber/Data/Research/data/theory_fragmentation_data/train/plain",
                                     4096,
                                     shuffle=True)
train_encrypted_reader = DirectoryReader("/Users/barber/Data/Research/data/theory_fragmentation_data/train/encrypted",
                                         4096,
                                         shuffle=True)
# TODO: Implement Batch here

validation_file_location = settings.read("validation_data", "location")
validation_file_begin = settings.read("validation_data", "begin")
validation_file_end = settings.read("validation_data", "end")
validation_files = [validation_file_location.format(i) for i in range(validation_file_begin, validation_file_end + 1)]

test_file_location = settings.read("test_data", "location")
test_file_begin = settings.read("test_data", "begin")
test_file_end = settings.read("test_data", "end")
test_files = [test_file_location.format(i) for i in range(test_file_begin, test_file_end + 1)]

train_queue = tf.train.string_input_producer(train_files, shuffle=True)
validation_queue = tf.train.string_input_producer(validation_files, shuffle=False)
test_queue = tf.train.string_input_producer(test_files, shuffle=False)

input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")
record_bytes = input_dimension + num_groups

train_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
validation_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
test_reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)

_, train_value = train_reader.read(train_queue)
_, validation_value = validation_reader.read(validation_queue)
_, test_value = test_reader.read(test_queue)

train_fragment = tf.cast(tf.decode_raw(train_value, tf.uint8), tf.float32)
validation_fragment = tf.cast(tf.decode_raw(validation_value, tf.uint8), tf.float32)
test_fragment = tf.cast(tf.decode_raw(test_value, tf.uint8), tf.float32)

train_fragment.set_shape([record_bytes])
validation_fragment.set_shape([record_bytes])
test_fragment.set_shape([record_bytes])

batch_size = settings.read("hyperparameters", "batch_size")
validation_batch_size = settings.read("test_info", "validation_batch_size")
test_batch_size = settings.read("test_info", "test_batch_size")
train_capacity = train_file_end - train_file_begin + 1

train_batch = tf.train.shuffle_batch([train_fragment],
                                     batch_size=batch_size,
                                     capacity=train_capacity,
                                     min_after_dequeue=batch_size)
validation_batch = tf.train.batch([validation_fragment], batch_size=validation_batch_size)
test_batch = tf.train.batch([test_fragment], batch_size=test_batch_size)

train_data, train_labels = tf.split(train_batch, [input_dimension, num_groups], 1)
validation_data, validation_labels = tf.split(validation_batch, [input_dimension, num_groups], 1)
test_data, test_labels = tf.split(test_batch, [input_dimension, num_groups], 1)
