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
@allure.feature('查询单个子账户持仓信息')
class TestSwapSubPositionInfo:

    def test_swap_sub_position_info(self, contract_code, sub_uid):
        r = t.swap_sub_position_info(contract_code=contract_code, sub_uid=sub_uid)
        schema = {
            "status": "ok",
            "ts": int,
            "data": [
                {
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "volume": float,
                    "available": float,
                    "frozen": float,
                    "cost_open": float,
                    "cost_hold": float,
                    "profit_unreal": float,
                    "profit_rate": float,
                    "profit": float,
                    "position_margin": float,
                    "lever_rate": int,
                    "direction": str,
                    "last_price": float
                }
            ]
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
