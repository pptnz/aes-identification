import caffe
import math
import os
import numpy as np
import unittest


class EncryptionChecker:
    """
    Checks given file fragment, in bfd form, is encrypted or not.
    Use the method of (1) Entropy or (2) CNN.
    """

    def __init__(self):
        """
        Initialize `EncryptionChecker` instance.
        """
        # Used for entropy_checker
        self.frequency_threshold = None
        self.entropy_threshold = None

        # Saves n * log(n) at table[n] to speedup entropy computation.
        self.entropy_lookup_table = None

        # Caffe CNN network
        self.cnn_network = None

        # Encryption threshold.
        self.encryption_threshold = None

    def setup_entropy_checker(self, frequency_threshold, entropy_threshold):
        """
        Setup the parameters of entropy checker.
        :param frequency_threshold: bfd value threshold.
                                    if bfd[i] >= frequency_threshold, the fragment will be classified as not-encrypted.
        :param entropy_threshold: bfd entropy value threshold.
                                if entropy(bfd) >= entropy_threshold, the fragment will be classified as not-encrypted.
                                Note that entropy(bfd) = sum(n * log(n)), not sum(-p * log(p)).
        """
        self.frequency_threshold = frequency_threshold

    def setup_cnn_checker(self, model_path, weight_path, encryption_threshold):
        """
        Setup the model and weight of cnn checker.
        :param model_path: path to caffe model file (like deploy.prototxt)
        :param weight_path: path to caffe weight file (like model.caffemodel)
        :param encryption_threshold: encryption threshold value.
                                     if CNN's encryption_probability >= encryption_threshold,
                                     the given fragment will be classified as encrypted.
        """
        self.cnn_network = caffe.Net(model_path, weight_path, caffe.TEST)
        self.cnn_network.blobs["data"].reshape(1, 1, 16, 16)
        self.encryption_threshold = encryption_threshold

    def check_by_entropy(self, bfd):
        """
        Checks whether given file fragment is encrypted or not, using entropy method.
        :param bfd: file fragment's bfd to check
        :return: 0, if given fragment is classified as non-encrypted.
                 1, if given fragment is classified as encrypted.
        """
        # Check the frequency
        if any(bfd_value >= self.frequency_threshold for bfd_value in bfd):
            # Plain Fragment
            return 0

        # Encrypted fragment
        return 1

    def check_by_cnn(self, bfd):
        """
        Checks whether given file fragment is encrypted or not, using CNN network.
        :param bfd: file fragment's bfd to check
        :return: 0, if given fragment is classified as non-encrypted.
                 1, if given fragment is classified as encrypted.
        """
        # Set CNN Network input
        cnn_input = np.reshape(np.asarray(bfd), newshape=[1, 16, 16])
        self.cnn_network.blobs["data"].data[...] = cnn_input

        # Run CNN Network
        cnn_result = self.cnn_network.forward()
        encryption_prob = cnn_result["prob"].tolist()[0][1]

        # Translate the result
        if encryption_prob >= self.encryption_threshold:
            # Encrypted Fragment
            return 1

        # Plain Fragment
        return 0


class EncryptionCheckerTest(unittest.TestCase):
    def setUp(self):
        self.plain_bfd = [0 for _ in range(256)]
        self.plain_bfd[0] = 2048
        self.plain_bfd[255] = 2048

        self.encrypted_bfd = [16 for _ in range(256)]

        self.encryption_checker = EncryptionChecker()
        self.encryption_checker.setup_entropy_checker(frequency_threshold=55,
                                                      entropy_threshold=16700)

        directory = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(directory, "caffemodel", "deploy.prototxt")
        weight_path = os.path.join(directory, "caffemodel", "model.caffemodel")
        self.encryption_checker.setup_cnn_checker(model_path=model_path,
                                                  weight_path=weight_path,
                                                  encryption_threshold=0.1)

    def test_check_by_entropy(self):
        self.assertEqual(self.encryption_checker.check_by_entropy(bfd=self.plain_bfd), 0)
        self.assertEqual(self.encryption_checker.check_by_entropy(bfd=self.encrypted_bfd), 1)

    def test_check_by_cnn(self):
        self.assertEqual(self.encryption_checker.check_by_cnn(bfd=self.plain_bfd), 0)
        self.assertEqual(self.encryption_checker.check_by_cnn(bfd=self.encrypted_bfd), 1)
