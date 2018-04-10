import tensorflow as tf
from input_tensor import input_tensor
from keep_prob import keep_prob
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")
data_type = eval(settings.read("hyperparameters", "data_type"))

bfd_casted = tf.map_fn(lambda t: tf.histogram_fixed_width(t, [0.0, 256.0], nbins=256, dtype=data_type),
                       input_tensor,
                       dtype=data_type)
bfd_reshaped = tf.reshape(bfd_casted, [-1, 16, 16, 1])

w1 = tf.get_variable(name='w1', shape=[7, 7, 1, 64], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
h1 = tf.nn.conv2d(bfd_reshaped, w1, strides=[1, 1, 1, 1], padding='SAME')
h1_pool = tf.nn.max_pool(h1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
h1_relu = tf.nn.relu(h1_pool)

w2 = tf.get_variable(name='w2', shape=[5, 5, 64, 128], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
h2 = tf.nn.conv2d(h1_relu, w2, strides=[1, 1, 1, 1], padding='SAME')
h2_pool = tf.nn.max_pool(h2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
h2_relu = tf.nn.relu(h2_pool)

w3 = tf.get_variable(name='w3', shape=[3, 3, 128, 256], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
h3 = tf.nn.conv2d(h2_relu, w3, strides=[1, 1, 1, 1], padding='SAME')
h3_pool = tf.nn.max_pool(h3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
h3_relu = tf.nn.relu(h3_pool)
h3_flat = tf.reshape(h3_relu, [-1, 1024])

w4 = tf.get_variable(name='w4', shape=[1024, 512], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
b4 = tf.Variable(tf.truncated_normal([512], dtype=data_type, stddev=0.1))
h4 = tf.nn.relu(tf.matmul(h3_flat, w4) + b4)
h4_drop = tf.nn.dropout(h4, keep_prob)

w5 = tf.get_variable(name='w5', shape=[512, 256], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
b5 = tf.Variable(tf.truncated_normal([256], dtype=data_type, stddev=0.1))
h5 = tf.nn.relu(tf.matmul(h4_drop, w5) + b5)
h5_drop = tf.nn.dropout(h5, keep_prob)

w6 = tf.Variable(tf.zeros([256, num_groups], dtype=data_type))
b6 = tf.Variable(tf.zeros([num_groups], dtype=data_type))
output_tensor = tf.nn.softmax(tf.matmul(h5_drop, w6) + b6)  # do not change the output tensor name.
