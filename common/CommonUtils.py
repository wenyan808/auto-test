#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/10 7:45 下午
# @Author  : yuhuiqing
import time
from common.redisComm import redisConf
import jsonpath
from config.conf import DEFAULT_CONTRACT_CODE

def retryUtil(func, *args):
    tryTimes = 1
    while True:
        func_info = func(args[0])
        if jsonpath.jsonpath(func_info,args[1]):
            break
        else:
            # 超过5次，跳过循环
            if tryTimes >= 5:
                break
            else:
                print('未返回预期数据，等待1秒，第', tryTimes, '次重试………………')
                tryTimes = tryTimes + 1
                time.sleep(1)
    return func_info

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