#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 7:45 下午
# @Author  : yuhuiqing
import time
from common.redisComm import redisConf
from config.conf import DEFAULT_CONTRACT_CODE

# 获取最新价
def currentPrice(contract_code=None):
    # 如果未传合约，获取默认
    if contract_code is None:
        contract_code = DEFAULT_CONTRACT_CODE
    # 创建redis客户端
    redisClient = redisConf('redis6379').instance()
    # 查询最新价
    last_price = str(redisClient.hmget('RsT:BILP:','CP:'+contract_code)[0]).split('#')[0]
    # 以2个小数点返回结果
    return round(float(last_price),2)

# 判断对手价是否存在
def opponentExist(symbol=None,asks=None,bids=None):
    # 创建redis客户端
    redisClient = redisConf('redis6379').instance()
    key = 'RsT:MarketBusinessPrice:'
    for i in range(3):
        result = str(list(redisClient.hmget(key,str('DEPTH.STEP0#HUOBI#'+symbol+'#1#')))[0]).split('#')[0]
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