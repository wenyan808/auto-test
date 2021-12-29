#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/19
# @Author  : HuiQing Yu

import logging
import traceback
import pymysql
from config.conf import MYSQL_CONF


class mysqlComm(object):

    def __init__(self):
        conf = eval(MYSQL_CONF)
        try:
            print("MYSQL CONN CONSTRUCTOR")
            self.__contract_conn = pymysql.connect(
                host=conf['host'], port=conf['port'], user=conf['userName'], password=conf['passwd'])
        except Exception as e:
            logging.warning('CONNECT MYSQL HOST FAILED')
            logging.warning(e)

    def selectdb_execute(self, dbSchema, sqlStr):
        print('数据库Schema:{}，执行sql ={}'.format(dbSchema, sqlStr))
        try:
            self.__contract_conn.ping(reconnect=True)
            self.__contract_conn.select_db(dbSchema)
            cursor = self.__contract_conn.cursor(
                cursor=pymysql.cursors.DictCursor)
            cursor.execute(sqlStr)
            self.__contract_conn.commit()
            data = cursor.fetchall()
            print('执行结果 = ' + str(data))
            return data
        except Exception as e:
            print(traceback.print_exc())
            print('SQL执行异常，操作回滚={}', str(e))
            self.__contract_conn.rollback()
            self.__contract_conn.close()
        finally:
            cursor.close()

    def __del__(self):
        try:
            print("MYSQL CONN DESTRUCTOR")
            self.__contract_conn.close()
        except Exception as e:
            print(e)

