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
@allure.feature('查询止盈止损订单历史委托')
class TestSwapTpslHisorders:

    def test_swap_tpsl_hisorders(self, contract_code):
        r = t.swap_tpsl_hisorders(contract_code=contract_code, status='0', create_date='7')
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
                    "tpsl_order_type": str,
                    "order_id": int,
                    "order_id_str": str,
                    "order_source": str,
                    "order_price": float,
                    "created_at": int,
                    "order_price_type": str,
                    "trigger_type": str,
                    "trigger_price": Or(int, float),
                    "status": int,
                    "source_order_id": Or(str, None),
                    "relation_tpsl_order_id": str,
                    "canceled_at": Or(int, None),
                    "fail_code": Or(str, None),
                    "fail_reason": Or(str, None),
                    "triggered_price": Or(float, None),
                    "relation_order_id": str,
                    "update_time": int
                }]
            },
            "ts": int
        }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
