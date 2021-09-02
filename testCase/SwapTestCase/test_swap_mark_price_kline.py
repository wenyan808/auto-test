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
@allure.feature('获取标记价格的K线数据')
class TestSwapMarkPriceKilne:

    def test_swap_mark_price_kline(self, contract_code):
        r = t.swap_mark_price_kline(contract_code=contract_code, period='1min', size='20')
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
                    "trade_turnover": str,
                    "amount": str
                }
            ],
            "status": "ok",
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
