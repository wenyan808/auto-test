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
@allure.feature('查询开仓单关联的止盈止损订单详情')
class TestSwapRelationTpslOrder:

    def test_swap_relation_tpsl_order(self, contract_code):
        a = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='50000',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        r = t.swap_relation_tpsl_order(contract_code=contract_code, order_id=a['data']['order_id'])


if __name__ == '__main__':
    pytest.main()
