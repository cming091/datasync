import json

from log.log_handler import LogHandler
logger = LogHandler(__name__)


class ioUtils:
    @staticmethod
    def formatOutput(output, value):
        try:
            if output == 'json':
                return json.dumps(value)
            elif output == 'int':
                return int(value)
            elif output == 'string':
                return str(value)
            elif output == 'listOne':
                if len(value) >= 1:
                    return value[0]
                else:
                    return ''
            else:
                return value
        except Exception as e:
            logger.exception(e)

    @staticmethod
    def getValueFromPath(path, line):
        data = line
        paths = path.split('.')
        for path in paths:
            data = data.get(path, {})
            if not data:
                if isinstance(data,int) or isinstance(data,float):
                   return data
                return ''
        return data

    @staticmethod
    def getAllfields(params):
        fields=[]
        for param in params:
            columns = param['columns']
            for field in columns:
                fields.append(field[2])
        return fields

    @staticmethod
    def filterData(optype, line):
        if optype == 'u':
            return {"op":optype,'_id':str(line['o2']['_id'])}
        elif optype== 'i' or optype=='d':
            return {"op":optype,'_id':str(line['o']['_id'])}
        return {}

    @staticmethod
    def checkDataValid(data, fields):
        for field in fields:
            if not data.get(field):
                return False
        return True