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
