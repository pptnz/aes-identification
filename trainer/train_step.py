import tensorflow as tf
from loss import loss
from global_step import global_step
from settings import Settings

settings = Settings("./settings.json")
learning_rate = settings.read("hyperparameters", "learning_rate")

train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss, global_step=global_step)
