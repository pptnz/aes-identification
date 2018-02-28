import tensorflow as tf
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
batch_size = settings.read("hyperparameters", "batch_size")

input_tensor = tf.placeholder(tf.float16, shape=[None, input_dimension])
