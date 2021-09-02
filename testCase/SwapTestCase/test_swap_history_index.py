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
@allure.feature('获取指数的K线数据')
class TestSwapHistoryIndex:

    def test_swap_history_index(self, contract_code):
        r = t.swap_history_index(symbol=contract_code, period='1min', size='1')
        schema = {
            "ch": str,
            "status": "ok",
            "ts": int,
            "data": [
                {
                    "id": Or(int, None),
                    "vol": Or(int, float, None),
                    "count":  Or(int, float, None),
                    "open":  Or(int, float, None),
                    "close":  Or(int, float, None),
                    "low":  Or(int, float, None),
                    "high":  Or(int, float, None),
                    "amount":  Or(int, float, None)
                }
            ]
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
