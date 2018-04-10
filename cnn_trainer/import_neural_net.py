import importlib


def import_neural_net(neural_net_name):
    neural_net_location = "neural_net.{}".format(neural_net_name)
    return importlib.import_module(neural_net_location)
