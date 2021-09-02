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
@allure.feature('获取跟踪委托当前委托')
class TestSwapTrackOpenorders:

    def test_swap_track_openorders(self, contract_code):
        t.swap_track_order(contract_code=contract_code,
                           direction='buy',
                           offset='open',
                           lever_rate='5',
                           volume='1',
                           callback_rate='0.01',
                           active_price='20000',
                           order_price_type='formula_price')
        r = t.swap_track_openorders(contract_code=contract_code)
        schema = {
            "status": "ok",
            "data": {
                "total_page": int,
                "total_size": int,
                "current_page": int,
                "orders": [{
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "volume": float,
                    "order_type": int,
                    "direction": str,
                    "offset": str,
                    "lever_rate": int,
                    "order_id": int,
                    "order_id_str": str,
                    "order_source": str,
                    "created_at": int,
                    "order_price_type": str,
                    "status": int,
                    "callback_rate": float,
                    "active_price": float,
                    "is_active": int
                }]
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
