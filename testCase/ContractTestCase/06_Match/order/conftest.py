#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/23 4:24 下午
# @Author  : yuhuiqing

import pytest
from common.mysqlComm import mysqlComm
from common.redisComm import redisConf

@pytest.fixture()
def redis6379():
    return redisConf('redis6379').instance()

@pytest.fixture()
def DB_orderSeq():
    return  mysqlComm('order_seq')