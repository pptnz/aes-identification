import lmdb
import caffe
from settings import Settings
from caffe.proto import caffe_pb2
from files_manager import FilesManager
from files import FileExhaustedError


class LMDBManager:
    settings = Settings()
    size = settings.read("fragment_size")
    batch_size = settings.read("batch_size")

    def __init__(self, path, files_manager):
        self.lmdb_env = lmdb.open(path, map_size=int(1e12))
        self.lmdb_txn = self.lmdb_env.begin(write=True)
        self.files_manager = files_manager
        self.item_key = 0
        self.manipulator = lambda x: x
        self.datum = caffe_pb2.Datum()

    def register_manipulator(self, manipulator):
        self.manipulator = manipulator

    def process(self):
        try:
            fragment = self.files_manager.get_fragment(size=self.size)
            while fragment is not None:
                data = self.manipulator(fragment)
                label = fragment.label
                self.datum = caffe.io.array_to_datum(data, label)
                item_key = '{:0>8d}'.format(self.item_key).encode('ascii')
                self.item_key += 1
                self.lmdb_txn.put(item_key, self.datum.SerializeToString())

                if self.item_key % self.batch_size == 0:
                    print("\t{} fragments processed".format(self.item_key))
                    self.lmdb_txn.commit()
                    self.lmdb_txn = self.lmdb_env.begin(write=True)

                fragment = self.files_manager.get_fragment(size=self.size)

            # last batch
            if self.item_key % self.batch_size != 0:
                self.lmdb_txn.commit()
                self.lmdb_txn = self.lmdb_env.begin(write=True)

        except FileExhaustedError:
            return
