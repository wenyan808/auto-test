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
@allure.feature('获取平台阶梯保证金')
class TestSwapLadderMargin:

    def test_swap_ladder_margin(self, contract_code):
        r = t.swap_ladder_margin(contract_code=contract_code)



if __name__ == '__main__':
    pytest.main()
