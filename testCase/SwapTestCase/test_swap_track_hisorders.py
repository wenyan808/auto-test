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
@allure.feature('获取跟踪委托历史委托')
class TestSwapTrackHisorders:

    def test_swap_track_hisorders(self, contract_code):
        r = t.swap_track_hisorders(contract_code=contract_code, status='0', trade_type='0', create_date='7')
        schema = {
            "status": "ok",
            "data": {
                "total_page": int,
                "total_size": int,
                "current_page": int,
                "orders": [{
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "triggered_price": Or(str, None),
                    "volume": float,
                    "order_type": int,
                    "direction": str,
                    "offset": str,
                    "lever_rate": int,
                    "order_id": int,
                    "order_id_str": str,
                    "order_source": str,
                    "created_at": int,
                    "update_time": int,
                    "order_price_type": str,
                    "status": int,
                    "canceled_at": int,
                    "fail_code": Or(int, None),
                    "fail_reason": Or(str, None),
                    "callback_rate": float,
                    "active_price": float,
                    "is_active": int,
                    "market_limit_price": Or(float, None),
                    "formula_price": Or(float, None),
                    "real_volume": Or(float, 0),
                    "relation_order_id": str
                }]
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
