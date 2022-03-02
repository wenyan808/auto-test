#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/10/01
# @Author  : HuiQing Yu


import pytest

from config import conf


# from tool.SwapTools import SwapTools


@pytest.fixture()
def contract_code():
    return conf.DEFAULT_CONTRACT_CODE


# @pytest.fixture()
# def latest_price():
#     return SwapTools.currentPrice()

@pytest.fixture()
def symbol():
    return conf.DEFAULT_SYMBOL

# @pytest.fixture()
# def SwapTool():
#     return SwapTools()
