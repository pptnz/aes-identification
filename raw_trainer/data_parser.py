import tensorflow as tf


class DataParser:
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data
        return self

    def decode_as_unit8(self):
        self.data = tf.decode_raw(self.data, tf.uint8)
        return self

    def set_shape(self, shape):
        self.data.set_shape(shape)
        return self

    def concat(self, data_to_concat):
        self.data = tf.concat([self.data, data_to_concat], axis=0)
        return self

    def cast(self, type_to_cast):
        self.data = tf.cast(self.data, type_to_cast)
        return self

    def get_data(self):
        return self.data
