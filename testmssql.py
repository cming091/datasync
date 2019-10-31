from config.configs.materials import Config

from dbs import Mssconn

cond = '10.20.1.9;cbwt;cbwt888999@;CBWT'
conp = '10.32.3.55;cbwp;iniT12#4;CBWP' 


if __name__=='__main__':
    print(str(Config))
    for sql in Config.sql:
        Mssconn.creatTable(sql,cond)
        print(Mssconn.fetchOne(sql,cond))

