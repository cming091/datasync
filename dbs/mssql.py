import pymssql
import time
from utils import retry,TError

from log.log_handler import LogHandler
logger = LogHandler(__name__)


class Mssconn():
    @staticmethod
    def getConnAndCur(params):
        params_list = params.split(';')
        conn = pymssql.connect(host=params_list[0],user=params_list[1],
                               password=params_list[2],database=params_list[3],
                               charset="utf8")
        cur = conn.cursor()
        return conn, cur

    @staticmethod
    def creatTable(sql, params):
        try:
            conn, cur = Mssconn.getConnAndCur(params)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def fetchOne(sql, params):
        try:
            conn, cur = Mssconn.getConnAndCur(params)
            cur.execute(sql)
            resList = cur.fetchone()
            cur.close()
            conn.close()
            return resList
        except Exception as e:
            logger.exception(e)



class Mssql():
    @retry
    def mssConnAndCur(self, params):
        logger.info('[output mssqldb config]:{}'.format(params))
        self.mssqlconn,self.mssqlcur = Mssconn.getConnAndCur(params)

    @retry
    def mssDelOne(self, data, flag):
        try:
            sql = "DELETE FROM {} WHERE {} =%s".format(self.table, self.unique)
            self.mssqlcur.execute(sql, str(data[0][self.unique]))
            if flag:
                self.mssqlconn.commit()
            logger.info('[op del sql]:{}'.format(data[0][self.unique]))
        except Exception as e:
            logger.exception(e)
            self.mssqlconn.rollback()
            raise TError("delOne")

    @retry
    def mssInsert(self, lines):
        try:
            for params in lines:
                params['utime'] = int(time.time())
                fields = list(self.fields)
                fields.append('utime')
                logger.info('[output fields]:{}'.format(fields))
                place = map(lambda x:'%s', params)
                sql = 'INSERT INTO {} ({}) VALUES ({}) '.format(self.table,','.join(fields),','.join(place))
                self.mssqlcur.execute(sql,tuple(params.values()))
                logger.info('[op insert sql]:{}'.format(tuple(list(params.values()))))
            self.mssqlconn.commit()
        except Exception as e:
            logger.exception(e)
            self.mssqlconn.rollback()
            raise TError("mInsert")

    def close(self):
        try:
            self.mssqlcur.close()
            self.mssqlconn.close()
        except Exception:
            pass