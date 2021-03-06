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
@allure.feature('合约下单')
class TestSwapOrder:

    def test_swap_order(self, contract_code):
        r = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='50000',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        coon = redis_config()
        field = "Order:#" + str(r['data']['order_id']) + "#1"

        if coon.hexists("RsT:APO:11448964#BTC-USD", field):
            pprint("下单APO更新验证成功")
        else:
            pprint("下单APO更新验证失败")
        # print(r)


if __name__ == '__main__':
    pytest.main()
