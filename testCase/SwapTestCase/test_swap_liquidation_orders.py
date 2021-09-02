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
@allure.feature('获取强平订单')
class TestSwapLiquidationOrders:

    def test_swap_liquidation_orders(self, contract_code):
        r = t.swap_liquidation_orders(contract_code=contract_code, trade_type='0', create_date='7', page_index='',
                                      page_size='')


if __name__ == '__main__':
    pytest.main()
