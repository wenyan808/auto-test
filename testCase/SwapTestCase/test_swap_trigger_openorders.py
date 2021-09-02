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
@allure.feature('获取计划委托当前委托')
class TestSwapTriggerOpenorders:

    def test_swap_trigger_openorders(self, contract_code):
        t.swap_trigger_order(contract_code=contract_code,
                             trigger_type='le',
                             trigger_price='50000',
                             order_price='50000',
                             order_price_type='limit',
                             volume='1',
                             direction='buy',
                             offset='open',
                             lever_rate='5')
        time.sleep(1)
        r = t.swap_trigger_openorders(contract_code=contract_code,
                                      page_index='',
                                      page_size='')

        schema = {
            "status": "ok",
            "data": {
                "orders": [
                    {
                        "symbol": "BTC",
                        "contract_code": "BTC-USD",
                        "trigger_type": "ge",
                        "volume": 4,
                        "order_type": 1,
                        "direction": "sell",
                        "offset": "open",
                        "lever_rate": 1,
                        "order_id": 23,
                        "order_id_str": "161251",
                        "order_source": "web",
                        "trigger_price": 2,
                        "order_price": 2,
                        "created_at": int,
                        "order_price_type": str,
                        "status": int
                    }],
                "total_page": int,
                "current_page": int,
                "total_size": int
            },
            "ts": int
        }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
