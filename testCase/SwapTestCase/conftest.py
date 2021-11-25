#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/01
# @Author  : HuiQing Yu

import pytest
from common.mysqlComm import mysqlComm
from common.redisComm import redisConf
from config import conf
from common.CommonUtils import currentPrice

@pytest.fixture()
def redis6379():
    return redisConf('redis6379').instance()

@pytest.fixture()
def DB_orderSeq():
    return  mysqlComm('order_seq')

@pytest.fixture()
def contract_code():
    contract_code = conf.DEFAULT_CONTRACT_CODE
    return contract_code

@pytest.fixture()
def latest_price():
    return currentPrice()

@pytest.fixture()
def symbol():
    symbol = conf.DEFAULT_SYMBOL
    return symbol