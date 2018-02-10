# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors
import codecs
import json
from logging import log
import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

class LolPipeline(object):
    

    @classmethod
    def from_settings(cls,settings):
        '''1、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。 
           2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
           3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams=dict(
            host=settings['MYSQL_HOST'],#读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',#编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool=adbapi.ConnectionPool('MySQLdb',**dbparams)#**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)#相当于dbpool付给了这个类，self中可以得到
    
    #得到连接池dbpool
    def __init__(self,dbpool):
        self.dbpool=dbpool

    #process_item方法是pipeline默认调用的，进行数据库操作
    def process_item(self, item, spider):
        query=self.dbpool.runInteraction(self._conditional_update,item)#调用update的方法
        query.addErrback(self._handle_error,item,spider)#调用异常处理方法
        return item

    #写入数据库中
    def _conditional_insert(self,tx,item):
        print("---------------这里是你想知道的tx---------------",tx)
        sql="insert into testpictures(name,url) values(%s,%s)"
        params=(item["name"],item["story"])
        tx.execute(sql,params)

    #错误处理方法
    def _handle_error(self, failue, item, spider):
        print (failue)

    #查询数据库
    def _conditional_select(self,tx,item):
        print("---------------这里是测试_conditional_select方法----------------")
        print("---------------这里是你想知道的tx---------------",tx)
        sql="select count(*) from summoner"
        tx.execute(sql)
        reponse = tx.fetchall()
        print(reponse)
    
    #更新数据库
    def _conditional_update(self,tx,item):
        print("---------------这里是执行_conditional_update方法----------------")
        try:
            print("----------------这里是测试update-------------------")
            sql="update summoner set story='%s' where first_name='%s' or last_name='%s'" %(item["story"],item["name"],item["name"])
            n = tx.execute(sql)
            print(n)
        except expression as identifier:
            raise identifier
        