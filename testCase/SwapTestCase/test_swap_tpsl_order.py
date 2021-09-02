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
@allure.feature('对仓位设置止盈止损订单')
class TestSwapTpslOrder:

    def test_swap_tpsl_order(self, contract_code):
        r = t.swap_tpsl_order(contract_code=contract_code,
                              direction='buy',
                              volume='1',
                              tp_trigger_price='20000',
                              tp_order_price_type='limit',
                              tp_order_price='20000')
        schema = {
            "status": "ok",
            "data": {
                "tp_order": {
                    "order_id": int,
                    "order_id_str": str
                },
                "sl_order": Or({
                    "order_id": int,
                    "order_id_str": str
                }, None)
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
