import copy
import pymongo
from bson.objectid import ObjectId
from utils import retry
from log.log_handler import LogHandler
logger = LogHandler(__name__)

class MCient():
    @staticmethod
    def getClient(uri):
        client = pymongo.MongoClient(uri)
        return client

    @staticmethod
    def getCollection(client, dbName, name):
        db = client[dbName]
        coll = db[name]
        return coll


class Mongo:
    @retry
    def mClient(self, uri, dbname, collection):
        if not hasattr(self,'client'):
            logger.info('[input mongo uri:{}\tdbname:{}\tcollection:{}]'.format(uri,dbname,collection))
            self.client  = MCient.getClient(uri)
            self.mclient = MCient.getCollection(self.client, dbname, collection)

    @retry
    def mAggregate(self, pattern, line):
        mpattern = copy.deepcopy(pattern)
        mpattern.append({'$match':{'_id':ObjectId(line['_id'])}})
        return list(self.mclient.aggregate(mpattern))

    @retry
    def mFind(self, pattern, line):
        pattern ={'_id':ObjectId(line['_id'])}
        return list(self.mclient.find(pattern))

    @retry
    def yFind(self, pattern):
        return self.mclient.find(pattern, no_cursor_timeout=True)#.limit(2)

    def close(self):
        try:
            self.client.close()
            del self.client
            del self.mclient
            del self.client
        except Exception as e:
            pass