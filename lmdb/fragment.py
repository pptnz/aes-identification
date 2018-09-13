import numpy as np
import unittest


class Fragment:
    def __init__(self, data, label):
        self.data = data
        self.label = label

    def histogram(self, shape):
        result = np.zeros(shape=[256])
        for i in range(len(self.data)):
            result[int(self.data[i])] += 1
        return np.reshape(result, newshape=shape)

    def multi_channel_histogram(self):
        result = np.zeros(shape=[256])
        for i in range(len(self.data)):
            result[int(self.data[i])] += 1
        multi_channel_result = np.repeat(result, 3)
        return np.reshape(multi_channel_result, newshape=[3, 16, 16])


class FragmentTest(unittest.TestCase):
    def setUp(self):
        self.fragment = Fragment(data=b'\x23\x45\x12\xfc', label=1)

    def test_histogram(self):
        print(self.fragment.histogram(shape=[1, 16, 16]))
