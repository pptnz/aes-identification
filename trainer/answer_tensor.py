import tensorflow as tf
from settings import Settings

settings = Settings("./settings.json")

batch_size = settings.read("hyperparameters", "batch_size")
num_groups = settings.read("data_info", "num_groups")

answer_tensor = tf.placeholder(tf.float32, shape=[batch_size, num_groups])
