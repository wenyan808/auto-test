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
@allure.feature('获取市场最近成交记录')
class TestSwapTrade:

    def test_swap_trade(self, contract_code):
        r = t.swap_trade(contract_code=contract_code)
        schema = {
            "ch": str,
            "status": "ok",
            "tick": {
                "data": [
                    {
                        "contract_code": str,
                        "amount": str,
                        "quantity": str,
                        "direction": str,
                        "id": int,
                        "price": str,
                        "ts": int
                    }
                ],
                "id": int,
                "ts": int
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
