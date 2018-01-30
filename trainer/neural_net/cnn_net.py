import tensorflow as tf
from input_tensor import input_tensor
from keep_prob import keep_prob
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")

input_tensor_reshaped = tf.reshape(input_tensor, [-1, 16, 16, 1])

w1 = tf.Variable(tf.truncated_normal([5, 5, 1, 2], stddev=0.1))
h1 = tf.nn.conv2d(input_tensor_reshaped, w1, strides=[1, 1, 1, 1], padding='SAME')
h1_pool = tf.nn.max_pool(h1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

w2 = tf.Variable(tf.truncated_normal([5, 5, 2, 4], stddev=0.1))
h2 = tf.nn.conv2d(h1_pool, w2, strides=[1, 1, 1, 1], padding='SAME')
h2_pool = tf.nn.max_pool(h2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

w3 = tf.Variable(tf.truncated_normal([5, 5, 4, 8], stddev=0.1))
h3 = tf.nn.conv2d(h2_pool, w3, strides=[1, 1, 1, 1], padding='SAME')
h3_pool = tf.nn.max_pool(h3, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
h3_flat = tf.reshape(h3_pool, [-1, 32])

w4 = tf.Variable(tf.truncated_normal([32, 8], stddev=0.1))
b4 = tf.Variable(tf.truncated_normal([8], stddev=0.1))
h4 = tf.nn.tanh(tf.matmul(h3_flat, w4) + b4)
h4_drop = tf.nn.dropout(h4, keep_prob)

w5 = tf.Variable(tf.zeros([8, num_groups]))
b5 = tf.Variable(tf.zeros([num_groups]))
output_tensor = tf.nn.softmax(tf.matmul(h4_drop, w5) + b5)  # do not change the output tensor name.
