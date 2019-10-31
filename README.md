### 执行 ###
设置环境变量 export ENV_CONF=dev 或者     export ENV_CONF=test
             export ENV_CONF=product     选择开发环境跟生产环境

usage python3 run.py argv           选择不同的功能配置

参数选项

‘’‘
inbound 入库
outbound 出库
materials 物料
boxes 箱子
’‘’

统一执行

sh start.sh dev|test|product


## 目录结构 ##
run.py 

config/
       configs/
            ...
       __init__.py     
core/
     __init__.py
     fetcher.py
     input.py
     output.py
dbs/
    __init__.py
    mongodb.py
    mssql.py
utils/
      __init__.py
      uemail.py
      uerror.py
      uio.py
log/
    __init__.py
    log_handler.py

start.sh

README.md

testmssql.py



### start.sh ###
- 启动

### run.py ###
- 应用入口

### config ###
- 配置

### readme.md ###
- 文档

### requirements.txt ###
依赖环境


