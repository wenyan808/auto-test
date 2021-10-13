#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan
import contextlib

import pytest
from common.ContractServiceAPI import t as ct
from config import conf
from logger import logger


@pytest.fixture()
def sub_uid():
    sub_uid_list = ct.contract_sub_account_list()
    sub_uid = sub_uid_list['data'][0]['sub_uid']
    return sub_uid


@pytest.fixture()
def symbol():
    symbol = conf.DEFAULT_SYMBOL
    return symbol


@pytest.fixture()
def test():
    test = 'testtest'
    return test

@pytest.fixture()
def symbol_period():
    symbol_period = conf.DEFAULT_CONTRACT_CODE
    return symbol_period


contract_types = {'CW': "this_week", 'NW': "next_week", 'CQ': "quarter", 'NQ': "next_quarter"}


@pytest.fixture()
def contract_type():
    return contract_types[conf.DEFAULT_CONTRACT_CODE[-2:]]

# 开仓
@pytest.fixture()
def offsetO():
    offset = 'open'
    return offset
# 平仓
@pytest.fixture()
def offsetC():
    offset = 'close'
    return offset

#买入
@pytest.fixture()
def directionB():
    direction = 'buy'
    return direction

#卖出
@pytest.fixture()
def directionS():
    direction = 'sell'
    return direction

# 杠杆
@pytest.fixture()
def lever_rate():
    lever_rate = 5
    return lever_rate

# 开仓
@pytest.fixture()
def offsetO():
    offset = 'open'
    return offset
# 平仓
@pytest.fixture()
def offsetC():
    offset = 'close'
    return offset

#买入
@pytest.fixture()
def directionB():
    direction = 'buy'
    return direction

#卖出
@pytest.fixture()
def directionS():
    direction = 'sell'
    return direction

# 杠杆
@pytest.fixture()
def lever_rate():
    lever_rate = 5
    return lever_rate

# 开仓
@pytest.fixture()
def offsetO():
    offset = 'open'
    return offset
# 平仓
@pytest.fixture()
def offsetC():
    offset = 'close'
    return offset

#买入
@pytest.fixture()
def directionB():
    direction = 'buy'
    return direction

#卖出
@pytest.fixture()
def directionS():
    direction = 'sell'
    return direction

# 杠杆
@pytest.fixture()
def lever_rate():
    lever_rate = 5
    return lever_rate