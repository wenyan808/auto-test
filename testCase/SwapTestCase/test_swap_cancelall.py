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
@allure.feature('全部撤单')
class TestSwapCancelall:

    def test_swap_cancelall(self, contract_code):
        i = 0
        while i < 11:
            i += 1
            t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='1',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        time.sleep(1)

        r = t.swap_cancelall(contract_code=contract_code)



if __name__ == '__main__':
    pytest.main()
