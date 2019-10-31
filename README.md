## 地址 ##
https://kintergration.chinacloudapp.cn:3000/chenshouming/datasync2.git

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
       bconfigs/
            ...
                          
core/
     fetcher.py
     input.py
     output.py
dbs/
    mongodb.py
    mssql.py
utils/
      util.py
log/
    log_handler.py

datastart.sh

README.md

mssql_test.py

mssql_test.py


### mssql_test.py ###
- 创建mssql数据库测试数据库

### mongo_test.py ###
- 测试mongo数据库

### datastart.sh ###
- 启动

### run.py ###
- 应用入口

### config ###
- 配置

### readme.md ###
- 文档

### fetcher.py ###
获取数据

### input.py ###
输入部分

### output.py ###
输出部分

### log ###
记录运行log
### requirements.txt ###
依赖环境



########crontab ########

0 8 * * *  cd /home/app/soft/kettle/datasync&&/bin/bash  /home/app/soft/kettle/datasync/datastart.sh 

0 0 1 * *  cd /home/app/soft/kettle/datasync&&/bin/bash  /home/app/soft/kettle/datasync/clean_log.sh 



