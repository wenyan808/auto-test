#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/19
# @Author  : HuiQing Yu

import logging
import traceback

import pymysql

from config.conf import MYSQL_CONF


class mysqlComm(object):

    def __init__(self, db):
            conf = eval(MYSQL_CONF)
            self.__host = conf[db]['host']
            self.__port = conf[db]['port']
            self.__userName = conf[db]['userName']
            self.__password = conf[db]['passwd']
            self.__dbName = conf[db]['dbName']
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

    def dictCursor(self, sqlStr):
        try:
            self.__db.ping(reconnect=True)
            cursor = self.__db.cursor(cursor=pymysql.cursors.DictCursor)
            cursor.execute(sqlStr)
            self.__db.commit()
            data = cursor.fetchall()
            print(f'执行sql = {sqlStr}')
            print(f'执行结果 = {data}')
            return data
        except Exception as e:
            print(traceback.print_exc())
            print(f'SQL执行异常，操作回滚={e}')
            self.__db.rollback()
            self.__db.close()