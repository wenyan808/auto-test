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
@allure.feature('查询开仓单关联的止盈止损订单详情')
class TestSwapRelationTpslOrder:

    def test_swap_relation_tpsl_order(self, contract_code):
        a = t.swap_order(contract_code=contract_code,
                         client_order_id='',
                         price='50000',
                         volume='1',
                         direction='buy',
                         offset='open',
                         lever_rate='5',
                         order_price_type='limit')
        r = t.swap_relation_tpsl_order(contract_code=contract_code, order_id=a['data']['order_id'])
        schema = {
            "status": "ok",
            "data": {
                "symbol": "BTC",
                "contract_code": "BTC-USD",
                "volume": int,
                "price": Or(int, float),
                "order_price_type": str,
                "direction": str,
                "offset": str,
                "lever_rate": int,
                "order_id": int,
                "order_id_str": str,
                "client_order_id": Or(int, None),
                "created_at": int,
                "trade_volume": int,
                "trade_turnover": Or(int, float),
                "fee": Or(int, float),
                "trade_avg_price": Or(int, float, None),
                "margin_frozen": float,
                "profit": Or(float, int),
                "status": int,
                "order_type": int,
                "order_source": str,
                "fee_asset": "BTC",
               # "liquidation_type": str,
                "canceled_at": int,
                "tpsl_order_info": [{
                    "volume": int,
                    "tpsl_order_type": str,
                    "direction": str,
                    "order_id": int,
                    "order_id_str": str,
                    "trigger_type": str,
                    "trigger_price": float,
                    "order_price": float,
                    "created_at": int,
                    "order_price_type": str,
                    "relation_tpsl_order_id": str,
                    "status": int,
                    "canceled_at": Or(int, None),
                    "fail_code": Or(int, None),
                    "fail_reason": Or(str, None),
                    "triggered_price": Or(float, None),
                    "relation_order_id": str
                }],
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
