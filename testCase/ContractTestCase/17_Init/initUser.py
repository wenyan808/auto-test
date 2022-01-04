#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/12/9
# @Author  : Alex Li
"""
用于纠错使用
"""

import time

from common.ContractServiceAPI import t as contract_api
from common.SwapMqComm import mqComm


if __name__ == '__main__':

    mq_result = mqComm.UserProductTriggerInitChannel(
        userId='11538447', symbol="BTC")
    if mq_result and mq_result['routed']:
        print('MQ信息发送成功……')
    else:
        assert False, 'MQ发送失败……'
    time.sleep(1)
