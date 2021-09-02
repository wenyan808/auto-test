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
@allure.feature('获取用户持仓信息')
class TestSwapPositionInfo:

    def test_swap_position_info(self, contract_code):
        r = t.swap_position_info(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "volume": Or(float, int),
                    "available": Or(float, int),
                    "frozen": Or(float, int),
                    "cost_open": Or(float, int),
                    "cost_hold": Or(float, int),
                    "profit_unreal": Or(float, int),
                    "profit_rate": Or(float, int),
                    "profit": Or(float, int),
                    "position_margin": Or(float, int),
                    "lever_rate": Or(float, int),
                    "direction": str,
                    "last_price": Or(float, int)
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
