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
@allure.feature('批量获取最近的交易记录')
class TestSwapHistoryTrade:

    def test_swap_history_trade(self, contract_code):
        r = t.swap_history_trade(contract_code=contract_code, size='1')
        schema = {
            "ch": str,
            "status": "ok",
            "ts": int,
            "data": [
                {
                    "id": Or(int, None),
                    "ts": int,
                    "data": [
                        {
                            "amount": Or(int, float),
                            "quantity": Or(int, float, None),
                            "direction": str,
                            "id": Or(int, None),
                            "price": Or(int, float),
                            "ts": int
                        }
                    ]
                }
            ]
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
