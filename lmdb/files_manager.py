import random
import unittest

from settings import Settings
from files import Files
from fragment import Fragment


class FilesManager:
    settings = Settings()

    def __init__(self, data_type):
        if data_type == 'train':
            plain_files = Files(path=self.settings.read("train", "plain"))
            encrypted_files = Files(path=self.settings.read("train", "encrypted"))
            num_fragments_per_type = self.settings.read("num_fragments_per_type", "train")
            self.index = 0
        else:
            plain_files = Files(path=self.settings.read("test", "plain"))
            encrypted_files = Files(path=self.settings.read("test", "encrypted"))
            num_fragments_per_type = self.settings.read("num_fragments_per_type", "test")
            if FilesManager.settings.read("skip_test_plain"):
                self.index = 1
            else:
                self.index = 0
        self.files = [plain_files, encrypted_files]
        self.index_pool = [0, 1]
        self.data_type = data_type
        self.num_fragments_left = [num_fragments_per_type] * 2

    def get_fragment(self, size):
        if self.data_type == 'train':
            index = random.sample(self.index_pool, 1)[0]
            if self.num_fragments_left[index] == 0:
                self.index_pool.remove(index)
                if len(self.index_pool) == 0:
                    # finished
                    return None
                index = self.index_pool[0]

            data = self.files[index].read(size=size)
            self.num_fragments_left[index] -= 1
            return Fragment(data=data, label=index)

        else:
            if self.num_fragments_left[self.index] == 0:
                self.index += 1
                if self.index >= 2:
                    # finished
                    return None

            data = self.files[self.index].read(size=size)
            self.num_fragments_left[self.index] -= 1
            return Fragment(data=data, label=self.index)


class FilesManagerTest(unittest.TestCase):
    def setUp(self):
        self.train_files_manager = FilesManager(data_type='train')
        self.test_files_manager = FilesManager(data_type='test')

    def test_train_files_manager(self):
        print("Train:")
        for _ in range(1000):
            fragment = self.train_files_manager.get_fragment(30)
            print("data=", fragment.data, "\nlabel=", fragment.label)

    def test_test_files_manager(self):
        print("Test:")
        for _ in range(1000):
            fragment = self.test_files_manager.get_fragment(30)
            print("data=", fragment.data, "\nlabel=", fragment.label)