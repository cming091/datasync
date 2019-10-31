from dbs import *
from utils import ioUtils,emailUtil

from log.log_handler import LogHandler
logger = LogHandler(__name__)


class Input(Mongo):
    def __init__(self, data, params:list):
        self.data = data
        self.param = params[0]

    def fieldStansfer(self, line, param):
        if param['db']['name'] == 'mClient':
            data = {}
            for column in param['columns']:
                data[column[2]] = \
                    ioUtils.formatOutput(column[1],
                    ioUtils.getValueFromPath(column[0],line))
            return data
        else:
            return line

    def dbInit(self):
        getattr(self, self.param['db']['name'])(*self.param['db']['params'])

    def getData(self, param, line):
        blocksList = []
        results = getattr(self, param['op']['fun'])(param['op']['params'], line)
        if results:
            for res in results:
                block = self.fieldStansfer(res, param)
                blocksList.append(block)
        return blocksList

    def work(self):
        self.dbInit()
        if not self.data:
            logger.info('[input over]')
            self.close()
            return
        for line in self.data:
            logger.info('[input in]:{}'.format(line))
            if not line:
                continue
            try:
                blocksList = self.getData(self.param, line)
            except Exception as e:
                logger.exception('[input error:{}]:{}'.format(str(e),line))
                emailUtil.sendMail('Input error', ' {} '.format(line))
                self.close()
                return
            if blocksList:
                logger.info('[input out ok]:{}'.format(blocksList))
                yield (line, blocksList)
        self.close()

    def __call__(self):
        return self.work()

