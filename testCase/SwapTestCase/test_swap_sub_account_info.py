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
@allure.feature('查询单个子账户资产信息')
class TestSwapSubAccountInfo:

    def test_swap_sub_account_info(self, sub_uid, contract_code):
        r = t.swap_sub_account_info(contract_code=contract_code, sub_uid=sub_uid)
        schema = {
            "status": "ok",
            "data": [
                {
                    "symbol": "BTC",
                    "contract_code": "BTC-USD",
                    "margin_balance": float,
                    "margin_position": Or(float, 0),
                    "margin_frozen": Or(float, 0),
                    "margin_available": float,
                    "profit_real": float,
                    "profit_unreal": Or(float, 0),
                    "withdraw_available": float,
                    "risk_rate": Or(float, None),
                    "liquidation_price": Or(float, None),
                    "adjust_factor": float,
                    "lever_rate": int,
                    "transfer_profit_ratio": Or(float, None),
                    "margin_static": float
                }
            ],
            "ts": int
        }
        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
