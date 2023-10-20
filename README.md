<div align="center">

# pywlf

*Common utils for python3.*

[![](https://img.shields.io/badge/pypi-latest-9cf.svg)](https://pypi.org/project/wlfutil/) [![](https://img.shields.io/badge/blog-@waisaa-blue.svg)](https://blog.csdn.net/qq_42761569?type=blog) [![](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/waisaa/tools-python3-wlf/tree/main/LICENSE)

</div>

pywlf provides a series of imperative functions that help deal with mysql, redis, influxdb and so on.

## Utils
| tool | desc |
|:---------:|:---------:|
| log | 日志操作工具类 |
| file | 文件目录操作方法集合|
| core | 通用操作方法集合|
| date | 日期操作方法集合|
| influxdb | Influxdb操作工具类|
| mysql | Mysql操作工具类|
| ssh | Shell操作工具类|
| minio | Minio操作工具类|
| redis | Redis操作工具类|
| kafka | Kafka操作工具类|
| http | Http操作工具类|

## Installation
```python3
pip3 install pywlf
```

## Quickuse
```python3
# 引入日志工具类
#from pywlf.log import LogUtil
# 引入文件目录操作方法集合中的某个方法
from pywlf.file import del_fd

log_name = 'run.log'
del_fd(log_file)
LogUtil.init(log_name, True)

LogUtil.info('title', 'this is a test')
```
