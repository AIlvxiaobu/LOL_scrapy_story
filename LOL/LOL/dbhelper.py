# -*- coding: utf-8 -*-

import MySQLdb
from scrapy.utils.project import get_project_settings #导入seetings配置
class dbhelper(object):

    #init方法，获取settings配置文件中的信息
    def __init__(self):
        self.settings=get_project_settings() #获取settings配置，设置需要的信息

        self.host=self.settings['MYSQL_HOST']
        self.port=self.settings['MYSQL_PORT']
        self.user=self.settings['MYSQL_USER']
        self.passwd=self.settings['MYSQL_PASSWD']
        self.db=self.settings['MYSQL_DBNAME']

    #连接到mysql，不是连接到具体的数据库
    def connectMysql(self):
        conn=MySQLdb.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             passwd=self.passwd,
                             charset='utf8') #要指定编码，否则中文可能乱码
        return conn

    #连接到具体的数据库（settings中设置的MYSQL_DBNAME）
    def connectDatabase(self):
        conn=MySQLdb.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             passwd=self.passwd,
                             db=self.db,
                             charset='utf8') #要指定编码，否则中文可能乱码
        return conn