#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/19
# @Author  : yuhuiqing
import threading

import pymysql

from config.conf import MYSQL_ORDERSEQ_CONF


class mysqlComm(object):
    # _instance_lock = threading.Lock()
    # _is_init = False

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(mysqlComm, "_instance"):
    #         with mysqlComm._instance_lock:
    #             if not hasattr(mysqlComm, "_instance"):
    #                 mysqlComm._instance = object.__new__(cls)
    #     return mysqlComm._instance

    def __init__(self, dbConf):

        # if not self._is_init:
        dbConfProperties = str(dbConf).split(';')
        self.__host = dbConfProperties[0]
        self.__port = int(dbConfProperties[1])
        self.__userName = dbConfProperties[2]
        self.__password = dbConfProperties[3]
        self.__dbName = dbConfProperties[4]
        try:
            self.__db = pymysql.connect(host=self.__host, port=self.__port, user=self.__userName,
                                        password=self.__password, database=self.__dbName)
            self._is_init = True
        except Exception as e:
            print('pymysql.connect Fail')
            print(e)

    def execute(self, sqlStr):
        try:
            cursor = self.__db.cursor()
            cursor.execute(sqlStr)
            self.__db.commit()
            data = cursor.fetchall()
            print('执行sql = ' + str(sqlStr))
            print('执行结果 = ' + str(data))
            return data
        except Exception as e:
            print('SQL执行异常，操作回滚={}', e)
            self.__db.rollback()
            self.__db.close()


orderSeq = mysqlComm(MYSQL_ORDERSEQ_CONF)
