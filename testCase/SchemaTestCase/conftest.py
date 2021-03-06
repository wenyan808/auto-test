#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan

import pytest
from common.SwapServiceAPI import t as st
from common.LinearServiceAPI import t as lt


@pytest.fixture()
def sub_uid():
    sub_uid_list = lt.linear_sub_account_list()
    sub_uid = sub_uid_list['data'][0]['sub_uid']
    return sub_uid


@pytest.fixture()
def contract_code():
    contract_code = 'BTC-USD'
    return contract_code


@pytest.fixture()
def symbol():
    symbol = 'BTC'
    return symbol



@pytest.fixture()
def linear_contract_code():
    contract_code = 'BTC-USDT'
    return contract_code
