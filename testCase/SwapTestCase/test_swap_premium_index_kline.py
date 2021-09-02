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
@allure.feature('获取溢价指数K线')
class TestSwapPremiumIndexKline:

    def test_swap_premium_index_kline(self, contract_code):
        r = t.swap_premium_index_kline(contract_code=contract_code, period='1min', size='20')
        schema = {
            "ch": str,
            "data": [
                {
                    "vol": str,
                    "close": str,
                    "count": str,
                    "high": str,
                    "id": int,
                    "low": str,
                    "open": str,
                    "amount": str
                }
            ],
            "status": "ok",
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
