from .base import BaseConfig

class Config(BaseConfig):
    name = 'outbound'
    sql = ["""
            CREATE TABLE outboundOrdersBase
            (
              _id VARCHAR(100) PRIMARY KEY
            , enter VARCHAR(100)
            , stock_type VARCHAR(100)
            , purchase_id VARCHAR(100)
            , code VARCHAR(100)
            , contract VARCHAR(100)
            , finish_time VARCHAR(100)
            , active_time VARCHAR(100)
            , work_begin VARCHAR(100)
            , work_end VARCHAR(100)
            , status INT
            , orders VARCHAR(100)
            , utime int default 0
            )
            ;
          """,
            """CREATE TABLE outboundOrdersMaterials
            (
              _id VARCHAR(100)
            , code VARCHAR(100)
            , materialsStatus INT
            , mid VARCHAR(100)
            , package VARCHAR(100)
            , materialsCode VARCHAR(100)
            , numCount INT
            , weight VARCHAR(100)
            , volume VARCHAR(100)
            , status INT
            , sapid VARCHAR(100)
            , utime int default 0
            )
            ;""",
           """CREATE TABLE outboundOrdersBoxes
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
            , utime int default 0
            )
            ;"""
           ]


    @property
    def config(self):
        return [{
            'fetcher': {
                        'name': 'mClient',
                        'params':self.setting['fParams'][0:3],
                        'pattern':{"ns": "{}.wms.outbound_orders".format(self.setting['fParams'][3])},
                        'freq': 24
                        },
            'input': [
                    {'db': {'name': 'mClient', 'params':[*self.setting['iParams'],'wms.outbound_orders'] },
                    'op': {'fun': 'mFind', 'params': {}},
                    'columns': [
                             ('from', 'string', 'enter'),
                             ('stock_type', 'string', 'stock_type'),
                             ('purchase_id', 'string', 'purchase_id'),
                             ('code', 'string', 'code'),
                             ('contract', 'string', 'contract'),
                             ('finish_time', 'string', 'finish_time'),
                             ('active_time', 'string', 'active_time'),
                             ('work_begin', 'string', 'work_begin'),
                             ('work_end', 'string', 'work_end'),
                             ('status', 'int', 'status'),
                             ('orders', 'listOne', 'orders'),
                             ('_id', 'string', '_id'),
                             ],
                    }
                     ],
            'output':
                {'db':
                    {'name': 'mssConnAndCur',
                     'params': self.setting['oParams'],
                     'table': 'outboundOrdersBase',
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
                'pattern': {"ns": "{}.wms.outbound_orders".format(self.setting['fParams'][3])},
                'freq': 24
            },
            'input': [
                {'db': {'name': 'mClient', 'params': [*self.setting['iParams'], 'wms.outbound_orders']},
                 'op': {'fun': 'mAggregate', 'params': [{"$unwind":"$materials"},{"$project":{"_id":1,'code':1,'status':1,'materials':1}}]},
                 'columns': [
                             ('_id', 'string', '_id'),
                             ('code', 'string', 'code'),
                             ('materials.status', 'int', 'materialsStatus'),
                             ('materials.mid', 'string', 'mid'),
                             ('materials.physics.package', 'string', 'package'),
                             ('materials.code', 'string', 'materialsCode'),
                             ('materials.count', 'int', 'numCount'),
                             ('materials.physics.weight', 'string', 'weight'),
                             ('materials.physics.volume', 'string', 'volume'),
                             ('materials.sapid', 'string', 'sapid'),
                             ('status', 'int', 'status'),
                             ],
                 }
            ],
            'output':
                {'db':
                     {'name': 'mssConnAndCur',
                      'params': self.setting['oParams'],
                      'table': 'outboundOrdersMaterials',
                      'unique': '_id'
                      },
                 'op':
                     {'fun': 'mssInsert'},
                 }
        },
        {
            'fetcher': {
                'name': 'mClient',
                'params': self.setting['fParams'][0:3],
                'pattern': {"ns": "{}.wms.outbound_orders".format(self.setting['fParams'][3])},
                'freq': 24
            },
            'input': [
                {'db': {'name': 'mClient', 'params': [*self.setting['iParams'], 'wms.outbound_orders']},
                 'op': {'fun': 'mAggregate', 'params': [{"$unwind":"$boxes"},{"$unwind":"$boxes.materials"},{"$project":{"_id":1,'code':1,'status':1,'boxes':1}}]},
                 'columns': [
                             ('_id', 'string', '_id'),
                             ('code', 'string', 'code'),
                             ('status', 'int', 'status'),
                             ('boxes.code', 'string', 'boxesCode'),
                             ('boxes.status', 'int', 'boxesStatus'),
                             ('boxes.materials.mid', 'string', 'mid'),
                             ('boxes.physics.package', 'string', 'package'),
                             ('boxes.materials.count', 'int', 'numCount'),
                             ('boxes.physics.weight', 'string', 'weight'),
                             ('boxes.physics.volume', 'string', 'volume'),
                             ('boxes.materials.sapid', 'string', 'sapid'),
                             ],
                 }
            ],
            'output':
                {'db':
                     {'name': 'mssConnAndCur',
                      'params': self.setting['oParams'],
                      'table': 'outboundOrdersBoxes',
                      'unique': '_id'
                      },
                 'op':
                     {'fun': 'mssInsert'},
                 }
        }
        ]


