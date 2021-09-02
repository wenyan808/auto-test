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
@allure.feature('批量获取子账户资产信息')
class TestSwapSubAccountInfoList:

    def test_swap_sub_account_info_list(self, contract_code):
        r = t.swap_sub_account_info_list(contract_code=contract_code)
        schema = {
            "status": "ok",
            "ts": int,
            "data": {
                "current_page": int,
                "total_page": int,
                "total_size": int,
                "sub_list": [{
                    "sub_uid": int,
                    "account_info_list": [{
                        "symbol": "BTC",
                        "contract_code": "BTC-USD",
                        "margin_balance": Or(float, 0),
                        "liquidation_price": Or(float, None),
                        "risk_rate": Or(float, None)
                    }
                    ]
                }]
            }
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
