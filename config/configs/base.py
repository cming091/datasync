class BaseConfig(object):
    def __init__(self, setting):
        self.setting = setting

    @property
    def pLen(self):
        return len(self.sql)

    @classmethod
    def __str__(cls):
        return str('[name:{} \t sql:{}]'.format(cls.name,cls.sql))



