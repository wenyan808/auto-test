#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/10/13
# @Author  : zhangranghan


from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema, And, Or, Regex, SchemaError

from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')
@allure.feature('批量获取最近的交易记录')
class TestSwapHistoryTrade:

    def test_swap_history_trade(self, contract_code):
        r = t.swap_history_trade(contract_code=contract_code, size='1')



if __name__ == '__main__':
    pytest.main()
