import lmdb
import caffe
import os
import numpy as np
from caffe.proto import caffe_pb2

# LMDB Preparation
if not os.path.exists("./lmdb"):
    os.makedirs("./lmdb")
lmdb_env = lmdb.open("./lmdb", map_size=int(1e12))
lmdb_txn = lmdb_env.begin(write=True)
item_key = 0
datum = caffe_pb2.Datum()

# Generate LMDB Value
value = [0, 0, 0, 0,
         0, 0, 0, 0,
         1, 1, 1, 1, 
         1, 1, 1, 1]
data = np.reshape(np.asarray(value), newshape=[1, 4, 4])
label = 0
datum = caffe.io.array_to_datum(data, label)
str_item_key = '{:0>8d}'.format(item_key).encode('ascii')
lmdb_txn.put(str_item_key, datum.SerializeToString())
item_key += 1

value = [0, 1, 1, 0,
         1, 0, 0, 1,
         1, 0, 0, 1, 
         0, 1, 1, 0]
data = np.reshape(np.asarray(value), newshape=[1, 4, 4])
label = 1
datum = caffe.io.array_to_datum(data, label)
str_item_key = '{:0>8d}'.format(item_key).encode('ascii')
lmdb_txn.put(str_item_key, datum.SerializeToString())
item_key += 1

value = [0, 0, 1, 1,
         0, 0, 1, 1,
         1, 1, 0, 0, 
         1, 1, 0, 0]
data = np.reshape(np.asarray(value), newshape=[1, 4, 4])
label = 2
datum = caffe.io.array_to_datum(data, label)
str_item_key = '{:0>8d}'.format(item_key).encode('ascii')
lmdb_txn.put(str_item_key, datum.SerializeToString())
item_key += 1

# Commit LMDB
lmdb_txn.commit()
