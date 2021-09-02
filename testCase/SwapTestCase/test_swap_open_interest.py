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
@allure.feature('量获取当前可用合约总持仓')
class TestSwapOpenInterest:

    def test_swap_open_interest(self, contract_code):
        r = t.swap_open_interest(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data":
                [{
                    "symbol": "BTC",
                    "volume": Or(float, int),
                    "amount": Or(float, int),
                    "trade_amount": Or(float, int),
                    "trade_volume": Or(float, int),
                    "trade_turnover": Or(float, int),
                    "contract_code": "BTC-USD"
                }],
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
