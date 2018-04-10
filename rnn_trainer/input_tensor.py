import tensorflow as tf
from settings import Settings

settings = Settings("./settings.json")
input_dimension = settings.read("data_info", "input_dimension")
batch_size = settings.read("hyperparameters", "batch_size")
data_type = eval(settings.read("hyperparameters", "data_type"))

input_tensor = tf.placeholder(data_type, shape=[None, input_dimension])
