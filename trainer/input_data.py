import tensorflow as tf
from settings import Settings

settings = Settings("./settings.json")

train_file_location = settings.read("train_data", "location")
train_file_begin = settings.read("train_data", "begin")
train_file_end = settings.read("train_data", "end")
train_files = [train_file_location.format(i) for i in range(train_file_begin, train_file_end + 1)]

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

train_reader = tf.TextLineReader()
validation_reader = tf.TextLineReader()
test_reader = tf.TextLineReader()

_, train_value = train_reader.read(train_queue)
_, validation_value = validation_reader.read(validation_queue)
_, test_value = test_reader.read(test_queue)

input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")
record_defaults = [[0.0] for _ in range(input_dimension + num_groups)]

train_fragment = tf.stack(tf.decode_csv(train_value, record_defaults=record_defaults))
validation_fragment = tf.stack(tf.decode_csv(validation_value, record_defaults=record_defaults))
test_fragment = tf.stack(tf.decode_csv(test_value, record_defaults=record_defaults))

batch_size = settings.read("hyperparameters", "batch_size")
num_fragments_per_csv = settings.read("data_info", "num_fragments_per_csv")

train_capacity = num_fragments_per_csv * (train_file_end - train_file_begin + 1)
min_after_dequeue = train_capacity - batch_size

train_batch = tf.train.shuffle_batch([train_fragment],
                                     batch_size=batch_size,
                                     capacity=train_capacity,
                                     # min_after_dequeue=min_after_dequeue)
                                     min_after_dequeue=batch_size)
# train_batch = tf.train.batch([train_fragment], batch_size=batch_size)
validation_batch = tf.train.batch([validation_fragment], batch_size=batch_size)
test_batch = tf.train.batch([test_fragment], batch_size=batch_size)

train_data, train_labels = tf.split(train_batch, [input_dimension, num_groups], 1)
validation_data, validation_labels = tf.split(validation_batch, [input_dimension, num_groups], 1)
test_data, test_labels = tf.split(test_batch, [input_dimension, num_groups], 1)
