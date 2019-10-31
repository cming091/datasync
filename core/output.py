import collections
from dbs.mssql import *
from log.log_handler import LogHandler
from utils import ioUtils,emailUtil

logger = LogHandler(__name__)


class Output(Mssql):
    def __init__(self, data, params:dict):
        self.data = data
        self.params = params
        self.table = self.params['output']['db']['table']
        self.unique = self.params['output']['db']['unique']

    def dbInit(self):
        getattr(self, self.params['output']['db']['name'])(self.params['output']['db']['params'])

    def delAndinsert(self, data, othermsg):
        if othermsg['op'] == 'd':
            self.mssDelOne(data, 1)
        else:
            self.mssDelOne(data, 0)
            getattr(self, self.params['output']['op']['fun'])(data)

    def sort(self, lines):
        newsortlinelist = []
        for line in lines:
            newsortline = collections.OrderedDict()
            for key in self.fields:
                newsortline[key] = line[key]
            newsortlinelist.append(newsortline)
        return newsortlinelist

    def work(self):
        self.dbInit()
        if not self.data:
            logger.info('[output over]')
            return
        self.fields =tuple(ioUtils.getAllfields(self.params['input']))
        for othermsg,lines in self.data:
            logger.info('[output in]:{}'.format(lines))
            if not lines:
               continue
            try:
                newsortlinelist = self.sort(lines)
                self.delAndinsert(newsortlinelist, othermsg)
            except Exception as e:
                logger.error('[output error:{}]:{}'.format(str(e),lines))
                emailUtil.sendMail('Output error', ' {} '.format(othermsg))
                return

            logger.info('[output out ok]:{}'.format(othermsg))

    def __call__(self):
        self.work()
        self.close()