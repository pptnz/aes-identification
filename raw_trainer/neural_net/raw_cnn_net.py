import tensorflow as tf
from input_tensor import input_tensor
from keep_prob import keep_prob
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")

input_tensor_reshaped = tf.reshape(input_tensor, [-1, 64, 64, 1])

w1 = tf.get_variable(name='w1', shape=[5, 5, 1, 2], dtype=tf.float16, initializer=tf.contrib.keras.initializers.he_normal())
h1 = tf.nn.conv2d(input_tensor_reshaped, w1, strides=[1, 1, 1, 1], padding='SAME')
h1_pool = tf.nn.max_pool(h1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

w2 = tf.get_variable(name='w2', shape=[5, 5, 2, 4], dtype=tf.float16, initializer=tf.contrib.keras.initializers.he_normal())
h2 = tf.nn.conv2d(h1_pool, w2, strides=[1, 1, 1, 1], padding='SAME')
h2_pool = tf.nn.max_pool(h2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

w3 = tf.get_variable(name='w3', shape=[5, 5, 4, 8], dtype=tf.float16, initializer=tf.contrib.keras.initializers.he_normal())
h3 = tf.nn.conv2d(h2_pool, w3, strides=[1, 1, 1, 1], padding='SAME')
h3_pool = tf.nn.max_pool(h3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

w4 = tf.get_variable(name='w4', shape=[5, 5, 8, 16], dtype=tf.float16, initializer=tf.contrib.keras.initializers.he_normal())
h4 = tf.nn.conv2d(h3_pool, w4, strides=[1, 1, 1, 1], padding='SAME')
h4_pool = tf.nn.max_pool(h4, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

w5 = tf.get_variable(name='w5', shape=[5, 5, 16, 32], dtype=tf.float16, initializer=tf.contrib.keras.initializers.he_normal())
h5 = tf.nn.conv2d(h4_pool, w5, strides=[1, 1, 1, 1], padding='SAME')
h5_pool = tf.nn.max_pool(h5, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
h5_flat = tf.reshape(h5_pool, [-1, 128])

w6 = tf.get_variable(name='w6', shape=[128, 16], dtype=tf.float16, initializer=tf.contrib.keras.initializers.he_normal())
b6 = tf.Variable(tf.truncated_normal([16], dtype=tf.float16, stddev=0.1))
h6 = tf.nn.tanh(tf.matmul(h5_flat, w6) + b6)
h6_drop = tf.nn.dropout(h6, keep_prob)

w7 = tf.Variable(tf.zeros([16, num_groups]))
b7 = tf.Variable(tf.zeros([num_groups]))
output_tensor = tf.nn.softmax(tf.matmul(h6_drop, w7) + b7)  # do not change the output tensor name.
