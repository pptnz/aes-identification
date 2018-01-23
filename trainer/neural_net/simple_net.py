import tensorflow as tf
from input_tensor import input_tensor
from keep_prob import keep_prob
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")

w1 = tf.Variable(tf.truncated_normal([input_dimension, 256]))
b1 = tf.Variable(tf.truncated_normal([256]))
hidden1 = tf.nn.relu(tf.matmul(input_tensor, w1) + b1)
hidden1_result = tf.nn.dropout(hidden1, keep_prob=keep_prob)

w0 = tf.Variable(tf.zeros([256, num_groups]))
b0 = tf.Variable(tf.zeros([num_groups]))
output_tensor = tf.nn.softmax(tf.matmul(hidden1_result, w0) + b0)  # do not change the output tensor name.
