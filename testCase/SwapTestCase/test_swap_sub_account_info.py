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
@allure.feature('查询单个子账户资产信息')
class TestSwapSubAccountInfo:

    def test_swap_sub_account_info(self, sub_uid, contract_code):
        r = t.swap_sub_account_info(contract_code=contract_code, sub_uid=sub_uid)


if __name__ == '__main__':
    pytest.main()
