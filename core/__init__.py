from multiprocessing.pool import Pool
from .fetcher import Oplog
from .input import Input
from .output import Output

class WorkFlow(object):
    def __init__(self, config):
        self.config = config

    def start(self, config):
        data = Oplog(config['fetcher'])()
        #data=[{'_id':'5c8342ca06160bf1e5d40180',"op":'i'}] #materials
        #data=[{'_id':'5c85c4d1233cac182ecff562',"op":'u'}] #testoutbase
        #data=[{'_id':'5c85caf36dfd9f196a377cea',"op":'i'}] #testoutmaterials
        #data=[{'_id':'5c85bdc64db380396af50c78',"op":'u'}] #testoutboxes
        #data=[{'_id':'5c85c7b3ac9e0cfd2d202a25',"op":'i'}] #testinboundbase
        #data=[{'_id':'5c85c7b3ac9e0cfd2d202a25',"op":'i'}]  #testinboundboxes
        idata = Input(data, config['input'])()
        Output(idata, config)()

    def pool(self):
        pool = Pool(processes=self.config.pLen)
        pool.map(self.start, self.config.config)
        pool.close()
        pool.join()



