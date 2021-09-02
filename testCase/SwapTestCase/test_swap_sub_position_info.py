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
@allure.feature('查询单个子账户持仓信息')
class TestSwapSubPositionInfo:

    def test_swap_sub_position_info(self, contract_code, sub_uid):
        r = t.swap_sub_position_info(contract_code=contract_code, sub_uid=sub_uid)


if __name__ == '__main__':
    pytest.main()
