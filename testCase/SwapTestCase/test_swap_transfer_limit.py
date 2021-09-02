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
@allure.feature('查询用户当前的划转限制')
class TestSwapTransferLimit:

    def test_swap_transfer_limit(self, contract_code):
        r = t.swap_transfer_limit(contract_code=contract_code)


if __name__ == '__main__':
    pytest.main()
