import tensorflow as tf
from settings import Settings
from import_neural_net import import_neural_net
from answer_tensor import answer_tensor


settings = Settings("./settings.json")
neural_net_name = settings.read("neural_net_info", "neural_net_name")
neural_net = import_neural_net(neural_net_name)
batch_size = settings.read("hyperparameters", "batch_size")
num_groups = settings.read("data_info", "num_groups")


loss = -tf.reduce_sum(answer_tensor * tf.log(neural_net.output_tensor))
