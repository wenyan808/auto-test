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
@allure.feature('获取平台历史结算记录')
class TestSwapSettlementRecords:

    def test_swap_settlement_records(self, contract_code):
        r = t.swap_settlement_records(contract_code=contract_code)
        schema = {
            "status": "ok",
            "ts": int,
            "data": {
                "settlement_record": [
                    {
                        "symbol": "BTC",
                        "contract_code": "BTC-USD",
                        "settlement_time": int,
                        "clawback_ratio": Or(float, 0),
                        "settlement_price": float,
                        "settlement_type": "settlement"
                    }
                ],
                "current_page": int,
                "total_page": int,
                "total_size": int
            }
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
