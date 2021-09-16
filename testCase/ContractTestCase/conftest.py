#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/7/31
# @Author  : zhangranghan

import pytest
from common.ContractServiceAPI import t as ct
from logger import logger


@pytest.fixture()
def sub_uid():
    sub_uid_list = ct.contract_sub_account_list()
    sub_uid = sub_uid_list['data'][0]['sub_uid']
    return sub_uid


@pytest.fixture()
def symbol():
    symbol = 'LTC'
    return symbol


@pytest.fixture()
def test():
    test = 'testtest'
    return test



@pytest.fixture()
def symbol_period():
    symbol_period = 'LTC_CW'
    return symbol_period