#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/17 3:29 下午
# @Author  : HuiQing Yu
import time

from common.mysqlComm import mysqlComm
from common.redisComm import redisConf
from config.conf import DEFAULT_CONTRACT_CODE,DEFAULT_SYMBOL


class SwapTools(object):

    def __init__(self):
        self.mysqlClient = mysqlComm()
        self.redis6379 = redisConf('redis6379').redisClient
        self.redis6380 = redisConf('redis6380').redisClient

    # 获取用户的资金信息
    def user_account(self,uid,symbol=None):
        """
            RsT:APO:11222677#BCH
            资金信息 Account:#BTC
        """
        if symbol is None:
            symbol = DEFAULT_SYMBOL
        key = f'RsT:APO:{uid}#{symbol}'
        fieldOfTheKey = f'Account:#{symbol}'
        # 信息映射BTC表t_account_capital字段
        account_capital = self.redis6380.hmget(key,fieldOfTheKey)
        # 如果没查到数据则返回None
        if len(account_capital) == 0:
            return None
        return account_capital[0]


    # 获取最新价
    def currentPrice(self, contract_code=None):
        # 如果未传合约，获取默认
        if contract_code is None:
            contract_code = DEFAULT_CONTRACT_CODE
        # 查询最新价
        last_price = str(self.redis6379.hmget('RsT:BILP:', 'CP:' + contract_code)[0]).split('#')[0]
        # 以2个小数点返回结果
        return round(float(last_price), 2)

    # 判断对手价是否存在
    def opponentExist(symbol=None, asks=None, bids=None):
        # 创建redis客户端
        redisClient = redisConf('redis6379').instance()
        key = 'RsT:MarketBusinessPrice:'
        for i in range(3):
            result = str(list(redisClient.hmget(key, str('DEPTH.STEP0#HUOBI#' + symbol + '#1#')))[0]).split('#')[0]
            result = eval(result)
            if asks is not None and bids is not None:
                if result['asks'] and result['asks']:
                    return True
            else:
                if asks is not None and result['asks']:
                    return True
                elif bids is not None and result['bids']:
                    return True

            # 到此则证明没有刷新,等待1秒再查一次
            time.sleep(1)
        return False

    # 获取结算中的合约
    def getSettlementContract(self):
        sqlStr = 'select product_id from t_product where  trade_status!=5 and init_status=0 limit 1'
        db_info = self.mysqlClient.selectdb_execute('contract_trade', sqlStr=sqlStr)
        if len(db_info) ==0:
            return None
        else:
            return db_info[0]['product_id']

# 调试区
SwapTool = SwapTools()
print(SwapTool.user_account(uid='11538483').split(',')[5])