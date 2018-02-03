import tensorflow as tf
from input_tensor import input_tensor
from keep_prob import keep_prob
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")

w1 = tf.get_variable(name='w1', shape=[input_dimension, 128], initializer=tf.contrib.keras.initializers.he_normal())
b1 = tf.Variable(tf.truncated_normal([128]))
hidden1 = tf.nn.relu(tf.matmul(input_tensor, w1) + b1)
hidden1_drop = tf.nn.dropout(hidden1, keep_prob)

w2 = tf.get_variable(name='w2', shape=[128, 256], initializer=tf.contrib.keras.initializers.he_normal())
b2 = tf.Variable(tf.truncated_normal([256]))
hidden2 = tf.nn.relu(tf.matmul(hidden1_drop, w2) + b2)
hidden2_drop = tf.nn.dropout(hidden2, keep_prob)

w3 = tf.get_variable(name='w3', shape=[256, 128], initializer=tf.contrib.keras.initializers.he_normal())
b3 = tf.Variable(tf.truncated_normal([128]))
hidden3 = tf.nn.tanh(tf.matmul(hidden2_drop, w3) + b3)
hidden3_drop = tf.nn.dropout(hidden3, keep_prob)

w4 = tf.get_variable(name='w4', shape=[128, 64], initializer=tf.contrib.keras.initializers.he_normal())
b4 = tf.Variable(tf.truncated_normal([64]))
hidden4 = tf.nn.tanh(tf.matmul(hidden3_drop, w4) + b4)
hidden4_drop = tf.nn.dropout(hidden4, keep_prob)

w5 = tf.get_variable(name='w5', shape=[64, 32], initializer=tf.contrib.keras.initializers.he_normal())
b5 = tf.Variable(tf.truncated_normal([32]))
hidden5 = tf.nn.tanh(tf.matmul(hidden4_drop, w5) + b5)
hidden5_drop = tf.nn.dropout(hidden5, keep_prob)

w6 = tf.get_variable(name='w6', shape=[32, 16], initializer=tf.contrib.keras.initializers.he_normal())
b6 = tf.Variable(tf.truncated_normal([16]))
hidden6_drop = tf.nn.tanh(tf.matmul(hidden5_drop, w6) + b6)

w7 = tf.get_variable(name='w7', shape=[16, 8], initializer=tf.contrib.keras.initializers.he_normal())
b7 = tf.Variable(tf.truncated_normal([8]))
hidden7_drop = tf.nn.tanh(tf.matmul(hidden6_drop, w7) + b7)

w8 = tf.get_variable(name='w8', shape=[8, 4], initializer=tf.contrib.keras.initializers.he_normal())
b8 = tf.Variable(tf.truncated_normal([4]))
hidden8 = tf.nn.tanh(tf.matmul(hidden7_drop, w8) + b8)

w9 = tf.Variable(tf.zeros([4, num_groups]))
b9 = tf.Variable(tf.zeros([num_groups]))
output_tensor = tf.nn.softmax(tf.matmul(hidden8, w9) + b9)  # do not change the output tensor name.
