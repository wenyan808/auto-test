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
    contract_code = 'BTC-USDT'
    return contract_code


@pytest.fixture()
def symbol():
    symbol = 'BTC'
    return symbol

@pytest.fixture()
def buy_price():
    buy_price = lt.linear_depth(contract_code='btc-usdt',type='step0')['tick']['bids'][0][0]
    return buy_price

@pytest.fixture()
def sell_price():
    sell_price = lt.linear_depth(contract_code='btc-usdt', type='step0')['tick']['asks'][0][0]
    return sell_price


@pytest.fixture()
def lever_rate():
    lever_rate = lt.linear_account_info(contract_code='btc-usdt')['data'][0]['lever_rate']
    return lever_rate


@pytest.fixture()
def last_price():
    last_price = lt.linear_history_trade(contract_code='btc-usdt', size='1')['data'][0]['data'][0]['price']
    return last_price
