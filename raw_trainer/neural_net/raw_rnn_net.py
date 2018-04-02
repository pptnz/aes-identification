# Reference
# Sentiment RNN : https://github.com/mchablani/deep-learning/blob/master/sentiment-rnn/Sentiment_RNN_Solution.ipynb
import tensorflow as tf
from input_tensor import input_tensor
from keep_prob import keep_prob
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
num_groups = settings.read("data_info", "num_groups")
data_type = eval(settings.read("hyperparameters", "data_type"))
batch_size = settings.read("hyperparameters", "batch_size")

lstm_width = 4096
lstm_depth = 2

num_byte_value = 256

# print(input_tensor)
input_tensor_one_hot = tf.one_hot(tf.reshape(input_tensor, [-1, 4096]), num_byte_value)

W = tf.Variable(tf.random_normal([lstm_width, num_groups]))
b = tf.Variable(tf.random_normal([num_groups]))


def lstm_cell():
    lstm = tf.nn.rnn_cell.BasicLSTMCell(lstm_width)
    return tf.nn.rnn_cell.DropoutWrapper(lstm, output_keep_prob=keep_prob)

cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell() for _ in range(lstm_depth)])

initial_state = cell.zero_state(batch_size, tf.float32)
outputs, states = tf.nn.dynamic_rnn(cell, input_tensor_one_hot, dtype=tf.float32, initial_state=initial_state)
pred = tf.contrib.layers.fully_connected(outputs[:, -1], 1, activation_fn=tf.sigmoid)

# fully connected layers
# 4096 - 1024 - 256 - 64 - 16 - 8 - 2
w1 = tf.get_variable(name='w1', shape=[lstm_width, 1024], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
b1 = tf.Variable(tf.truncated_normal([1024], dtype=data_type, stddev=0.1))
h1 = tf.nn.tanh(tf.matmul(pred, w1) + b1)
h1_drop = tf.nn.dropout(h1, keep_prob)

w2 = tf.get_variable(name='w2', shape=[1024, 256], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
b2 = tf.Variable(tf.truncated_normal([1024], dtype=data_type, stddev=0.1))
h2 = tf.nn.tanh(tf.matmul(h1_drop, w2) + b2)
h2_drop = tf.nn.dropout(h2, keep_prob)

w3 = tf.get_variable(name='w3', shape=[256, 64], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
b3 = tf.Variable(tf.truncated_normal([64], dtype=data_type, stddev=0.1))
h3 = tf.nn.tanh(tf.matmul(h2_drop, w3) + b3)
h3_drop = tf.nn.dropout(h3, keep_prob)

w4 = tf.get_variable(name='w4', shape=[64, 16], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
b4 = tf.Variable(tf.truncated_normal([16], dtype=data_type, stddev=0.1))
h4 = tf.nn.tanh(tf.matmul(h3_drop, w4) + b4)
h4_drop = tf.nn.dropout(h4, keep_prob)

w5 = tf.get_variable(name='w5', shape=[16, 8], dtype=data_type, initializer=tf.contrib.keras.initializers.he_normal())
b5 = tf.Variable(tf.truncated_normal([8], dtype=data_type, stddev=0.1))
h5 = tf.nn.tanh(tf.matmul(h4_drop, w5) + b5)
h5_drop = tf.nn.dropout(h5, keep_prob)

w6 = tf.Variable(tf.zeros([8, num_groups], dtype=data_type))
b6 = tf.Variable(tf.zeros([num_groups], dtype=data_type))
output_tensor = tf.nn.softmax(tf.matmul(h5_drop, w6) + b6)  # do not change the output tensor name.

