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

lstm_width = 512
lstm_input = 64
lstm_step = 64
lstm_depth = 3

num_byte_value = 256


# Abandon one-hot encoding due to the speed.
# input_tensor_casted = tf.cast(input_tensor, tf.int32)
# input_tensor_one_hot = tf.one_hot(input_tensor_casted, num_byte_value)
input_tensor_reshaped = tf.reshape(input_tensor, [-1, lstm_input, lstm_step])


W = tf.Variable(tf.random_normal([lstm_width, num_groups]))
b = tf.Variable(tf.random_normal([num_groups]))


def lstm_cell():
    lstm = tf.nn.rnn_cell.BasicLSTMCell(lstm_width)
    return tf.nn.rnn_cell.DropoutWrapper(lstm, output_keep_prob=keep_prob)

cell = tf.nn.rnn_cell.MultiRNNCell([lstm_cell() for _ in range(lstm_depth)])

outputs, states = tf.nn.dynamic_rnn(cell, input_tensor_reshaped, dtype=data_type)

output_tensor = tf.contrib.layers.fully_connected(outputs[:, -1], num_groups, activation_fn=tf.sigmoid)
