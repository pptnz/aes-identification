import tensorflow as tf
from loss import loss
from global_step import global_step
from settings import Settings

settings = Settings("./settings.json")
learning_rate = settings.read("hyperparameters", "learning_rate")
epsilon = settings.read("hyperparameters", "epsilon")
"""
optimizer = tf.train.AdamOptimizer(learning_rate, epsilon=epsilon)
gvs = optimizer.compute_gradients(loss)
capped_gvs = [(tf.clip_by_value(grad, -1., 1.), var) for grad, var in gvs]
train_step = optimizer.apply_gradients(capped_gvs, global_step=global_step)
"""
train_step = tf.train.AdamOptimizer(learning_rate, epsilon=epsilon).minimize(loss, global_step=global_step)
