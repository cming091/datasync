from .base import BaseConfig

class Config(BaseConfig):
    name = 'materials'
    sql = ["""
           CREATE TABLE materials
            (
              _id VARCHAR(100) PRIMARY KEY
            , id VARCHAR(100)
            , first_time VARCHAR(100)
            , unit VARCHAR(100)
            , utime int default 0
            )
            ;"""]


    @property
    def config(self):
        return [{
            'fetcher': {
                'name': 'mClient',
                'params': self.setting['fParams'][0:3],
                'pattern': {"ns": "{}.wms.outbound_orders".format(self.setting['fParams'][3])},
                'freq': 24
            },
            'input': [
                {'db': {'name': 'mClient', 'params': [*self.setting['iParams'], 'wms.materials']},
                 'op': {'fun': 'mFind', 'params': {}},
                 'columns': [('id', 'string', 'id'),
                             ('first_time', 'string', 'first_time'),
                             ('unit', 'string', 'unit'),

                             ('_id', 'string', '_id'),
                             ],
                 }
            ],
            'output':
                {'db':
                     {'name': 'mssConnAndCur',
                      'params': self.setting['oParams'],
                      'table': 'materials',
                      'unique': '_id'
                      },
                 'op':
                     {'fun': 'mssInsert'},
                 }
        }]

