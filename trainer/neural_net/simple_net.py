import tensorflow as tf
from input_tensor import input_tensor
from keep_prob import keep_prob
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")

w1 = tf.Variable(tf.truncated_normal([input_dimension, 128]))
b1 = tf.Variable(tf.truncated_normal([128]))
hidden1 = tf.nn.tanh(tf.matmul(input_tensor, w1) + b1)
hidden1_drop = tf.nn.dropout(hidden1, keep_prob)

w2 = tf.Variable(tf.truncated_normal([128, 64]))
b2 = tf.Variable(tf.truncated_normal([64]))
hidden2 = tf.nn.tanh(tf.matmul(hidden1_drop, w2) + b2)
hidden2_drop = tf.nn.dropout(hidden2, keep_prob)

w3 = tf.Variable(tf.truncated_normal([64, 32]))
b3 = tf.Variable(tf.truncated_normal([32]))
hidden3 = tf.nn.tanh(tf.matmul(hidden2_drop, w3) + b3)
hidden3_drop = tf.nn.dropout(hidden3, keep_prob)

w4 = tf.Variable(tf.truncated_normal([32, 16]))
b4 = tf.Variable(tf.truncated_normal([16]))
hidden4 = tf.nn.tanh(tf.matmul(hidden3_drop, w4) + b4)
hidden4_drop = tf.nn.dropout(hidden4, keep_prob)

w5 = tf.Variable(tf.truncated_normal([16, 8]))
b5 = tf.Variable(tf.truncated_normal([8]))
hidden5 = tf.nn.tanh(tf.matmul(hidden4_drop, w5) + b5)
hidden5_drop = tf.nn.dropout(hidden5, keep_prob)

w6 = tf.Variable(tf.truncated_normal([8, 4]))
b6 = tf.Variable(tf.truncated_normal([4]))
hidden6 = tf.nn.tanh(tf.matmul(hidden5_drop, w6) + b6)

w7 = tf.Variable(tf.zeros([4, num_groups]))
b7 = tf.Variable(tf.zeros([num_groups]))
output_tensor = tf.nn.softmax(tf.matmul(hidden6, w7) + b7)  # do not change the output tensor name.
