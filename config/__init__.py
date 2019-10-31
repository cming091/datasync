
class Settings(object):
    email=('test@163.com',
           'cming091',
           'kettle',
           ['test@163.com'],
           'smtp.163.com',)
    retryTimes = 2
    logPath = '/Users/mac/Desktop/product2/datasync2/log/log'

    @staticmethod
    def getSetting(env, name):
        print('Settings---{}---{}\n'.format(env,name))
        envs = {
            "test": {
                     "fParams": ['mongodb://opread:opreadabc@127,0.0.1', 'local','oplog.rs','wms_530'],
                     "iParams": ['mongodb://wms_530:wms_530bgh@127.0.0.1/wms_530', 'wms_530'],
                     "oParams": '127.0.0.1;SA;Aa123456;test',
                     },
            "dev": {
                    "fParams":[],
                     "iParams": [],
                     "oParams": '',
                     },

            "product": {
                     "fParams": [],
                     "iParams": [],
                     "oParams": '',
                     },
        }
        settings = {
                    'materials': 'config.configs.materials',
                    'outbound': 'config.configs.outbound',
                    'inbound':'config.configs.inbound',
                    'boxes':'config.configs.boxes',
                    }
        return settings[name], envs[env]
