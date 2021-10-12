#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan

import pytest
from common.SwapServiceAPI import t as st
from config import conf


@pytest.fixture()
def sub_uid():
    sub_uid_list = st.swap_sub_account_list()
    sub_uid = sub_uid_list['data'][0]['sub_uid']
    return sub_uid


@pytest.fixture()
def contract_code():
    contract_code = conf.DEFAULT_CONTRACT_CODE
    return contract_code

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