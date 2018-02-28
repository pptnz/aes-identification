import tensorflow as tf
from loss import loss
from global_step import global_step
from settings import Settings

settings = Settings("./settings.json")
learning_rate = settings.read("hyperparameters", "learning_rate")
epsilon = settings.read("hyperparameters", "epsilon")

train_step = tf.train.AdamOptimizer(learning_rate, epsilon=epsilon).minimize(loss, global_step=global_step)
