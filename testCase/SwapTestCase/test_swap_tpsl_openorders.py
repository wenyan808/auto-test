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
@allure.feature('查询止盈止损订单当前委托')
class TestSwapTpslOpenorders:

    def test_swap_tpsl_openorders(self, contract_code):
        t.swap_tpsl_order(contract_code=contract_code,
                          direction='buy',
                          volume='1',
                          tp_trigger_price='20000',
                          tp_order_price_type='limit',
                          tp_order_price='20000')
        r = t.swap_tpsl_openorders(contract_code=contract_code)
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
                    "tpsl_order_type": str,
                    "direction": str,
                    "order_id": int,
                    "order_id_str": str,
                    "order_source": str,
                    "order_price": float,
                    "trigger_type": str,
                    "trigger_price": float,
                    "created_at": int,
                    "order_price_type": str,
                    "status": int,
                    "source_order_id": Or(str, None),
                    "relation_tpsl_order_id": str
                }]
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
