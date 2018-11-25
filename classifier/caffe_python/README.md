# encryption_checker
엔트로피와 CNN을 이용하여, 데이터셋의 암호화 유무를 판단한 후 파일에 저장합니다.

## Dependencies
- `python3`을 이용합니다.
```bash
$ sudo apt install python3
```

- `python3`에서 import 가능한 `caffe`가 설치되어야 합니다. ([Caffe Installation](http://caffe.berkeleyvision.org/installation.html#compilation))
```bash
# Caffe Dependencies
$ sudo apt build-dep caffe-cpu
$ sudo apt install cmake libopenblas-dev
$ pip3 install numpy

# Clone and Compile Caffe
$ git clone https://github.com/BVLC/caffe.git /path/to/install/caffe
$ cd /path/to/install/caffe
$ mkdir build
$ cd build
$ cmake .. -DCPU_ONLY=ON -DBLAS=open -Dpython_version=3
$ make all
$ make install
$ make runtest

# Export PYTHONPATH
$ export PYTHONPATH=/path/to/install/caffe/python:$PYTHONPATH
```

## 사용법
1. `settings.json`을 수정합니다.
주로 수정해야 하는 정보는 `non_media`와 `media` 데이터셋 파일의 위치, 그리고 결과가 출력될 파일입니다.
```json
{
  "non_media": {
    "input": "./data/media.file",
    "output": {
      "entropy": "./result/non_media_entropy.txt",
      "cnn": "./result/non_media_cnn.txt"
    }
  },

  "media": {
    "input": "./data/media.file",
    "output": {
      "entropy": "./result/media_entropy.txt",
      "cnn": "./result/media_cnn.txt"
    }
  },
  
  "fragment_size": 4096,

  "entropy_checker": {
    "frequency_threshold": 55,
    "entropy_threshold": 16700
  },

  "cnn_checker": {
    "model_path": "./caffemodel/deploy.prototxt",
    "weight_path": "./caffemodel/model.caffemodel",
    "encryption_threshold": 0.1
  }
}
```

2. `main.py`를 실행합니다.
```bash
$ python3 main.py
```

3. 결과 파일에는 데이터 조각이 암호화되지 않았으면 0, 암호화되었으면 1을 각 줄마다 기록합니다.
```
# non_media_cnn.txt
# non_media 데이터셋을 cnn을 이용하여 분류한 결과
0
0
0
0
1
1
0
1
1
...
```
