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
@allure.feature('获取计划委托历史委托')
class TestSwapTriggerHisorders:

    def test_swap_trigger_hisorders(self, contract_code):
        r = t.swap_trigger_hisorders(contract_code=contract_code,
                                     trade_type='0',
                                     status='0',
                                     create_date='7',
                                     page_index='',
                                     page_size='')
        schema = {
            "status": "ok",
            "data": {
                "orders": [
                    {
                        "symbol": str,
                        "contract_code": str,
                        "trigger_type": str,
                        "volume": float,
                        "order_type": int,
                        "direction": str,
                        "offset": str,
                        "lever_rate": int,
                        "order_id": int,
                        "order_id_str": str,
                        "relation_order_id": str,
                        "order_price_type": str,
                        "status": int,
                        "order_source": str,
                        "trigger_price": float,
                        "triggered_price": Or(float, None),
                        "order_price": float,
                        "created_at": int,
                        "triggered_at": Or(int, None),
                        "order_insert_at": int,
                        "canceled_at": int,
                        "fail_code": Or(int, None),
                        "fail_reason": Or(str, None),
                        "update_time": int
                    }
                ],
                "total_page": int,
                "current_page": int,
                "total_size": int
            },
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == 'S__main__':
    pytest.main()
