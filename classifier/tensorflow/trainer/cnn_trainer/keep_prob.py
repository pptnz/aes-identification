import tensorflow as tf
from settings import Settings

settings = Settings("./settings.json")
data_type = eval(settings.read("hyperparameters", "data_type"))

keep_prob = tf.placeholder(data_type)
