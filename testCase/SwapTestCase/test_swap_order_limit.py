#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020/8/24
# @Author  : zhangranghan


from common.SwapServiceAPI import t
from tool.get_test_data import case_data
from schema import Schema, And, Or, Regex, SchemaError

from pprint import pprint
import pytest, allure, random, time


@allure.epic('反向永续')
@allure.feature('查询用户当前的下单量限制')
class TestSwapOrderLimit:

    def test_swap_order_limit(self, contract_code):
        r = t.swap_order_limit(contract_code=contract_code,
                               order_price_type='limit')
        schema = {
            "status": "ok",
            "data": {
                "order_price_type": str,
                "list": [
                    {
                        "symbol": "BTC",
                        "contract_code": "BTC-USD",
                        "open_limit": Or(float, int),
                        "close_limit": Or(float, int)
                    }
                ]
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
