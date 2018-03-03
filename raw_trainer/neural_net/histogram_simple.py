import tensorflow as tf
from input_tensor import input_tensor
from keep_prob import keep_prob
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")
data_type = eval(settings.read("hyperparameters", "data_type"))

# input_tensor_casted = tf.cast(input_tensor, tf.int32)
bfd_casted = tf.map_fn(lambda t: tf.histogram_fixed_width(t, [0.0, 256.0], nbins=32, dtype=data_type),
                       input_tensor,
                       dtype=data_type)

w1 = tf.get_variable(name='w1', shape=[32, 8], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
b1 = tf.Variable(tf.truncated_normal([8], dtype=data_type, stddev=0.1))
h1 = tf.nn.tanh(tf.matmul(bfd_casted, w1) + b1)
h1_drop = tf.nn.dropout(h1, keep_prob)

w2 = tf.Variable(tf.zeros([8, num_groups], dtype=data_type))
b2 = tf.Variable(tf.zeros([num_groups], dtype=data_type))
output_tensor = tf.nn.softmax(tf.matmul(h1_drop, w2) + b2)  # do not change the output tensor name.
