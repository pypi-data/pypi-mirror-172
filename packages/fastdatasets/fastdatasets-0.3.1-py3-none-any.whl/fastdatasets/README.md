## datasets for tfrecords

### RecordWrite
```python
import data_serialize
from fastdatasets import RecordLoader,TFRecordOptions,TFRecordCompressionType,TFRecordWriter,gfile
#写二进制特征
def test_write_featrue():
    options = TFRecordOptions(compression_type=TFRecordCompressionType.NONE)
    def test_write(filename, N=3, context='aaa'):
        with TFRecordWriter(filename, options=options) as file_writer:
            for _ in range(N):
                val1 = data_serialize.Int64List(value=[1, 2, 3] * 20)
                val2 = data_serialize.FloatList(value=[1, 2, 3] * 20)
                val3 = data_serialize.BytesList(value=[b'The china', b'boy'])
                featrue = data_serialize.Features(feature=
                {
                    "item_0": data_serialize.Feature(int64_list=val1),
                    "item_1": data_serialize.Feature(float_list=val2),
                    "item_2": data_serialize.Feature(bytes_list=val3)
                }
                )
                example = data_serialize.Example(features=featrue)
                file_writer.write(example.SerializeToString())

    test_write('d:/example.tfrecords0',3,'file0')
    test_write('d:/example.tfrecords1',10,'file1')
    test_write('d:/example.tfrecords2',12,'file2')
#写任意字符串
def test_write_string():
    options = TFRecordOptions(compression_type=TFRecordCompressionType.NONE)
    def test_write(filename, N=3, context='aaa'):
        with TFRecordWriter(filename, options=options) as file_writer:
            for _ in range(N):
                # x, y = np.random.random(), np.random.random()
                file_writer.write(context + '____' + str(_))

    test_write('d:/example.tfrecords0',3,'file0')
    test_write('d:/example.tfrecords1',10,'file1')
    test_write('d:/example.tfrecords2',12,'file2')



```

### Simple Writer Demo
```python
import pickle
import data_serialize
from fastdatasets import RecordLoader,FeatrueWriter,StringWriter,PickleWriter,DataType,gfile

def test_string(filename=r'd:\\example_writer.record0'):
    print('test_string ...')
    with StringWriter(filename) as writer:
        for i in range(2):
            writer.write(b'123' )

    datasets = RecordLoader.IterableDataset(filename)
    for i,d in enumerate(datasets):
        print(i, d)

def test_pickle(filename=r'd:\\example_writer.record1'):
    print('test_pickle ...')

    with PickleWriter(filename) as writer:
        for i in range(2):
            writer.write(b'test_pickle' + b'123')
    datasets = RecordLoader.RandomDataset(filename)
    datasets = datasets.map(lambda x: pickle.loads(x))
    for i in range(len(datasets)):
        print(i, datasets[i])

def test_feature(filename=r'd:\\example_writer.record2'):
    print('test_feature ...')
    with FeatrueWriter(filename) as writer:
        for i in range(3):
            feature = {
                'input_ids': {
                    'dtype': DataType.int64_list,
                    'data': list(range(i + 1))
                },
                'seg_ids': {
                    'dtype': DataType.float_list,
                    'data': [i,0,1,2]
                },
                'other':{
                    'dtype': DataType.bytes_list,
                    'data': [b'aaa',b'bbbc1']
                },
            }
            writer.write(feature)


    datasets = RecordLoader.RandomDataset(filename)
    for i in range(len(datasets)):
        example = data_serialize.Example()
        example.ParseFromString(datasets[i])
        feature = example.features.feature
        print(feature)

test_string()
test_pickle()
test_feature()

```

### IterableDataset demo

```python
import data_serialize
from fastdatasets import RecordLoader,TFRecordOptions,TFRecordCompressionType,TFRecordWriter,gfile

data_path = gfile.glob('d:/example.tfrecords*')
options = TFRecordOptions(compression_type=None)
base_dataset = RecordLoader.IterableDataset(data_path_or_data_iterator=data_path,cycle_length=1,
                                            block_length=1,
                                            buffer_size=128,
                                            options=options,
                                            with_share_memory=True)
def test_batch():
    num = 0
    for _ in base_dataset:
        num +=1
    print('base_dataset num',num)
    
    base_dataset.reset()
    ds = base_dataset.repeat(2).repeat(2).repeat(3).map(lambda x:x+bytes('_aaaaaaaaaaaaaa',encoding='utf-8'))
    num = 0
    for _ in ds:
        num +=1
    
    print('repeat(2).repeat(2).repeat(3) num ',num)


def test_torch():
    def filter_fn(x):
        if x == b'file2____2':
            return True
        return False

    base_dataset.reset()
    dataset = base_dataset.filter(filter_fn).interval(2,0)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)
        
        
    base_dataset.reset()
    dataset = base_dataset.batch(3)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)
    
    # torch.utils.data.IterableDataset
    from fastdatasets.torch_dataset import IterableDataset
    dataset.reset()
    ds = IterableDataset(dataset=dataset)
    for d in ds:
        print(d)


def test_mutiprocess():
    print('mutiprocess 0...')
    base_dataset.reset()
    dataset = base_dataset.mutiprocess(process_num=3,process_id=0)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)
    
    print('mutiprocess 1...')
    base_dataset.reset()
    dataset = base_dataset.mutiprocess(process_num=3,process_id=1)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)
    
    print('mutiprocess 2...')
    base_dataset.reset()
    dataset = base_dataset.mutiprocess(process_num=3,process_id=2)
    i = 0
    for d in dataset:
        i += 1
        print(i,d)

```



### RandomDataset demo 
```python
from fastdatasets import RecordLoader,TFRecordOptions,TFRecordCompressionType,TFRecordWriter,gfile

data_path = gfile.glob('d:/example.tfrecords*')
options = TFRecordOptions(compression_type=None)
dataset = RecordLoader.RandomDataset(data_path_or_data_list=data_path,options=options,
                                            with_share_memory=True)


dataset = dataset.map(lambda x: x+  b"adasdasdasd")
print(len(dataset))

for i in range(len(dataset)):
    print(i+1,dataset[i])

print('batch...')
dataset = dataset.batch(7)
for i in range(len(dataset)):
    print(i+1,dataset[i])

print('unbatch...')
dataset = dataset.unbatch()
for i in range(len(dataset)):
    print(i+1,dataset[i])

print('shuffle...')
dataset = dataset.shuffle(10)
for i in range(len(dataset)):
    print(i+1,dataset[i])

print('map...')
dataset = dataset.map(transform_fn=lambda x:x + b'aa22222222222222222222222222222')
for i in range(len(dataset)):
    print(i+1,dataset[i])

print('torch Dataset...')
from fastdatasets.torch_dataset import Dataset

d = Dataset(dataset)
for i in range(len(d)):
    print(i + 1,d[i])


```

### IterableDataset demo2 

```python
import data_serialize
from fastdatasets import RecordLoader,TFRecordOptions,TFRecordCompressionType,TFRecordWriter,gfile

options = TFRecordOptions(compression_type=None)
data = [iter(range(10)),iter(range(10))]

base_dataset = RecordLoader.IterableDataset(data_path_or_data_iterator=data,
                                           cycle_length=1,block_length=1,buffer_size=128,options=options,
                                            with_share_memory=True)

for i,d in enumerate(base_dataset):
    print(i,d)
print('shuffle...')
base_dataset.reset()
base_dataset = base_dataset.shuffle(10)
for i,d in enumerate(base_dataset):
    print(i,d)
```


### RandomDataset demo2
```python
import data_serialize
from fastdatasets import RecordLoader,TFRecordOptions,TFRecordCompressionType,TFRecordWriter,gfile

data_path = [list(range(15)),list(range(15))]
options = TFRecordOptions(compression_type=None)
dataset = RecordLoader.RandomDataset(data_path_or_data_list=data_path, options=options,
                                            with_share_memory=True)

for i in range(len(dataset)):
    print(i + 1, dataset[i])

dataset = dataset.map(lambda x: str(x) +  "asdsadasaaaaaaaa")
print(len(dataset))

for i in range(len(dataset)):
    print(i + 1, dataset[i])

print('batch...')
dataset = dataset.batch(7)
for i in range(len(dataset)):
    print(i + 1, dataset[i])

print('unbatch...')
dataset = dataset.unbatch()
for i in range(len(dataset)):
    print(i + 1, dataset[i])

print('shuffle...')
dataset = dataset.shuffle(10)
for i in range(len(dataset)):
    print(i + 1, dataset[i])
#
# print('map...')
# dataset = dataset.map(transform_fn=lambda x: x + b'aa22222222222222222222222222222')
# for i in range(len(dataset)):
#     print(i + 1, dataset[i])

print('torch Dataset...')
from fastdatasets.torch_dataset import Dataset

d = Dataset(dataset)
for i in range(len(d)):
    print(i + 1, d[i])
```