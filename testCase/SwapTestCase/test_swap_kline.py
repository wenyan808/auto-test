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
@allure.feature('获取K线数据')
class TestSwapKline:

    def test_swap_kline(self, contract_code):
        r = t.swap_kline(contract_code=contract_code, period='1min', size='20', From='', to='')



if __name__ == '__main__':
    pytest.main()
