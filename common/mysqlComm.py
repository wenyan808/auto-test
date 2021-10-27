#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/19
# @Author  : yuhuiqing
import threading

import pymysql

from config.conf import MYSQL_ORDERSEQ_CONF
import traceback,pprint
import logging

class mysqlComm(object):

    def __init__(self, dbConf):
            dbConfProperties = str(dbConf).split(';')
            self.__host = dbConfProperties[0]
            self.__port = int(dbConfProperties[1])
            self.__userName = dbConfProperties[2]
            self.__password = dbConfProperties[3]
            self.__dbName = dbConfProperties[4]
            try:
                self.__db = pymysql.connect(host=self.__host, port=self.__port, user=self.__userName,
                                            password=self.__password, database=self.__dbName)
            except Exception as e:
                logging.warning('pymysql.connect Fail')
                logging.warning(e)

    def execute(self, sqlStr):
        try:
            self.__db.ping(reconnect=True)
            cursor = self.__db.cursor()
            cursor.execute(sqlStr)
            self.__db.commit()
            data = cursor.fetchall()
            print('执行sql = ' + str(sqlStr))
            print('执行结果 = ' + str(data))
            return data
        except Exception as e:
            print(traceback.print_exc())
            print('SQL执行异常，操作回滚={}', str(e))
            self.__db.rollback()
            self.__db.close()


orderSeq = mysqlComm(MYSQL_ORDERSEQ_CONF)