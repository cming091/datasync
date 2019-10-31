import time
from dbs import *
from bson.timestamp import Timestamp
from utils import ioUtils,emailUtil
from log.log_handler import LogHandler
logger = LogHandler(__name__)

class Oplog(Mongo):
    now = int(time.time())

    def __init__(self, param: dict):
        self.param = param

    def dbInit(self):
        if not hasattr(self, 'mclient'):
            getattr(self,self.param['name'])(*self.param['params'])

    def find(self):
        pattern = self.param['pattern']
        pattern.update({'ts':
                            {'$gte': Timestamp(self.now - self.param['freq'] * 60 * 60, 0),
                            "$lt": Timestamp(self.now, 0)
                             }
                        })
        logger.info('[fetcher config]:{}'.format(self.param))
        return (ioUtils.filterData(i['op'], i) for i in self.yFind(pattern))

    def __call__(self):
        try:
            self.dbInit()
            return self.find()
        except Exception as e:
            logger.exception(e)
            emailUtil.sendMail('Fetcher error', '获取数据失败')
            return None
        finally:
            self.close()

