import sys
import os
import importlib

from core import WorkFlow
from config import Settings
from utils import emailUtil


env = os.environ.get("ENV_CONF", 0)
if not env:
    print("请输入 os.environ.set('ENV_CONF') 对应的 env 环境\t export ENV_CONF=")
    os._exit(0)

def init():
    pass

def main():
    if len(sys.argv) != 2:
        print('usage python run.py argv')
        os._exit(0)

    """ init """
    _ = init()

    """ config """
    module, envSetting = Settings.getSetting(env,sys.argv[1])
    Config = importlib.import_module(module).Config
    config = Config(envSetting)

    """ schedule """
    workflow = WorkFlow(config)
    if env == 'test':
        workflow.start(config.config[0])
    else:
        workflow.pool()

    """ end """
    emailUtil.endSign()



if __name__=="__main__":
    main()
