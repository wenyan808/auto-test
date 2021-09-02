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
@allure.feature('获取合约最高限价和最低限价')
class TestSwapPriceLimit:

    def test_swap_price_limit(self, contract_code):
        r = t.swap_price_limit(contract_code=contract_code)


if __name__ == '__main__':
    pytest.main()
