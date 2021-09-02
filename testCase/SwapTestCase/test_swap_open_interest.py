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
@allure.feature('量获取当前可用合约总持仓')
class TestSwapOpenInterest:

    def test_swap_open_interest(self, contract_code):
        r = t.swap_open_interest(contract_code=contract_code)


if __name__ == '__main__':
    pytest.main()
