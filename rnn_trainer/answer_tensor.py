import tensorflow as tf
from settings import Settings

settings = Settings("./settings.json")

batch_size = settings.read("hyperparameters", "batch_size")
num_groups = settings.read("data_info", "num_groups")
data_type = eval(settings.read("hyperparameters", "data_type"))

answer_tensor = tf.placeholder(data_type, shape=[batch_size, num_groups])
