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
@allure.feature('撤销订单')
class TestSwapCancel:

    def test_swap_cancel(self, contract_code):
        a = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='1',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        time.sleep(1)
        r = t.swap_cancel(contract_code=contract_code,
                          order_id=a['data']['order_id'])


if __name__ == '__main__':
    pytest.main()
