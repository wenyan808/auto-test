#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/01
# @Author  : HuiQing Yu

import pytest
from config import conf


@pytest.fixture()
def contract_code():
    contract_code = conf.DEFAULT_CONTRACT_CODE
    return contract_code


@pytest.fixture()
def symbol():
    symbol = conf.DEFAULT_SYMBOL
    return symbol