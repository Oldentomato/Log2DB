# Log2DB 
[![PyPI Latest Release](https://img.shields.io/pypi/v/log2db.svg)](https://pypi.org/project/log2db/)
![Package Format](https://img.shields.io/pypi/format/log2db.svg)
![Python Version](https://img.shields.io/pypi/pyversions/log2db.svg)
[![Package Status](https://img.shields.io/pypi/status/log2db.svg)](https://pypi.org/project/log2db/)
[![GitHub](https://img.shields.io/github/license/oldentomato/Log2DB)](https://github.com/Oldentomato/Log2DB/blob/main/LICENSE) 
[![Build Version](https://img.shields.io/github/v/release/oldentomato/Log2DB)](https://github.com/Oldentomato/Log2DB/releases)

> DeepLearning Log Send to DB Module  

## Introdution
Log2DB is a tool that uploads, manages, and visualizes simple deep learning logs to your own DB.  

## How To Install 
- Download manually:  
https://github.com/Oldentomato/Log2DB/releases  

Download PyPI:
```sh
pip install log2db
```

## How To Use 
- Basic preparation
```python
import log2db as lgdb

#Set the DB Server 
db = lgdb.SetMongoDB(db_url = 'db_url',
                    db_document_name='doc',
                    db_collection_name='coll',
                    port=12345)
coll = db.Connect_DB()
sendlog = lgdb.SendLog(coll)
```
- example
```python
sendlog.on_train_start(
    model_name = 'pytorch_test',
    experiment_count = 3,
    datas_count = len(x_data),
    epoch = 100,
    batch_size = 8,
    learning_rate = 0.01,
    criterion = 'CrossEntropyLoss',
    optimizer = 'SGD(momentum=0.5)',
    model_shape = model,
    LR_scheduler = 'None',
    etc = 'None'
)

...

sendlog.on_epoch_end(epoch=epoch, loss=loss, val_loss=val_loss, acc=acc, val_acc=val_acc)

...

sendmoel.on_train_end(save_graph_url=True)
```

## Dependency
- **Pandas** https://github.com/pandas-dev/pandas
- **Matplotlib** https://github.com/matplotlib/matplotlib
- **pymongo** https://github.com/mongodb/mongo-python-driver
- **scikit-learn** https://github.com/scikit-learn/scikit-learn  


## License
[MIT](LICENSE)


