from .base import BaseConfig

class Config(BaseConfig):
    name = 'inbound'
    sql = ["""
            CREATE TABLE inboundOrdersBase
            (
              _id VARCHAR(100) PRIMARY KEY
            , ito VARCHAR(100)
            , stock_type VARCHAR(100)
            , purchase_id VARCHAR(100)
            , code VARCHAR(100)
            , contract VARCHAR(100)
            , status INT
            , utime int default 0
            )
            ;
          """,
            """CREATE TABLE inboundOrdersBoxesMaterials
            (
              _id VARCHAR(100)
            , boxesCode VARCHAR(100)
            , mid VARCHAR(100)
            , package VARCHAR(100)
            , weight VARCHAR(100)
            , volume VARCHAR(100)
            , boxesStatus INT
            , sapid VARCHAR(100)
            , code VARCHAR(100)
            , numCount INT
            , status INT
            , carriage_time VARCHAR(100)
            , utime int default 0
            )
            ;""",
           ]


    @property
    def config(self):
        return [{
            'fetcher': {
                        'name': 'mClient',
                        'params':self.setting['fParams'][0:3],
                        'pattern':{"ns": "{}.wms.inbound_orders".format(self.setting['fParams'][3])},
                        'freq': 24
                        },
            'input': [
                    {'db': {'name': 'mClient', 'params':[*self.setting['iParams'],'wms.inbound_orders'] },
                    'op': {'fun': 'mFind', 'params': {}},
                    'columns': [
                             ('to', 'string', 'ito'),
                             ('stock_type', 'string', 'stock_type'),
                             ('purchase_id', 'string', 'purchase_id'),
                             ('code', 'string', 'code'),
                             ('contract', 'string', 'contract'),
                             ('status', 'int', 'status'),
                             ('_id', 'string', '_id'),
                             ],
                    }
                     ],
            'output':
                {'db':
                    {'name': 'mssConnAndCur',
                     'params': self.setting['oParams'],
                     'table': 'inboundOrdersBase',
                     'unique':'_id'
                     },
                 'op':
                     {'fun': 'mssInsert'},
                 }
        },
        {
            'fetcher': {
                'name': 'mClient',
                'params': self.setting['fParams'][0:3],
                'pattern': {"ns": "{}.wms.inbound_orders".format(self.setting['fParams'][3])},
                'freq': 24
            },
            'input': [
                {'db': {'name': 'mClient', 'params': [*self.setting['iParams'], 'wms.inbound_orders']},
                 'op': {'fun': 'mAggregate', 'params': [{"$unwind":"$boxes"},{"$unwind":"$boxes.materials"},{"$project":{"_id":1,'code':1,'status':1,'boxes':1}}]},
                 'columns': [
                             ('_id', 'string', '_id'),
                             ('code', 'string', 'code'),
                             ('status', 'int', 'status'),
                             ('boxes.status', 'int', 'boxesStatus'),
                             ('boxes.code', 'string', 'boxesCode'),
                             ('boxes.carriage_time', 'string', 'carriage_time'),
                             ('boxes.materials.mid', 'string', 'mid'),
                             ('boxes.materials.sapid', 'string', 'sapid'),
                             ('boxes.materials.count', 'int', 'numCount'),
                             ('boxes.physics.package', 'string', 'package'),
                             ('boxes.physics.weight', 'string', 'weight'),
                             ('boxes.physics.volume', 'string', 'volume'),
                             ],
                 }
            ],
            'output':
                {'db':
                     {'name': 'mssConnAndCur',
                      'params': self.setting['oParams'],
                      'table': 'inboundOrdersBoxesMaterials',
                      'unique': '_id'
                      },
                 'op':
                     {'fun': 'mssInsert'},
                 }
        }
        ]


