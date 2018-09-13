import os
from settings import Settings
from lmdb_manager import LMDBManager
from files_manager import FilesManager


def main():
    settings = Settings()

    def manipulator(data):
        return data.histogram(shape=[1, 16, 16])

    if settings.read("num_fragments_per_type", "train") == 0:
        print("Skipping Train Fragments.")
    else:
        print("Generating Train Fragments...")

        train_result_path = settings.read("result", "train")
        if not os.path.exists(train_result_path):
            os.makedirs(train_result_path)

        train_files_manager = FilesManager(data_type='train')
        train_lmdb_manager = LMDBManager(path=train_result_path, files_manager=train_files_manager)
        train_lmdb_manager.register_manipulator(manipulator=manipulator)

        train_lmdb_manager.process()

    if settings.read("num_fragments_per_type", "test") == 0:
        print("Skipping Test Fragments.")
    else:
        print("Generating Test Fragments...")

        test_result_path = settings.read("result", "test")
        if not os.path.exists(test_result_path):
            os.makedirs(test_result_path)

        test_files_manager = FilesManager(data_type='test')
        test_lmdb_manager = LMDBManager(path=test_result_path, files_manager=test_files_manager)
        test_lmdb_manager.register_manipulator(manipulator=manipulator)

        test_lmdb_manager.process()


if __name__ == '__main__':
    main()
