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
@allure.feature('查询用户结算记录')
class TestSwapUserSettlementRecords:

    def test_swap_user_settlement_records(self, contract_code):
        r = t.swap_user_settlement_records(contract_code=contract_code, start_time='', end_time='', page_index='1',
                                           page_size='10')

        schema = {
            "status": "ok",
            "data": {
                "settlement_records": [
                    {
                        "symbol": str,
                        "contract_code": str,
                        "margin_balance_init": float,
                        "margin_balance": float,
                        "settlement_profit_real": float,
                        "settlement_time": int,
                        "clawback": float,
                        "funding_fee": float,
                        "offset_profitloss": float,
                        "fee": float,
                        "fee_asset": str,
                        "positions": [
                            {
                                "symbol": str,
                                "contract_code": str,
                                "direction": str,
                                "volume": float,
                                "cost_open": float,
                                "cost_hold_pre": float,
                                "cost_hold": float,
                                "settlement_profit_unreal": float,
                                "settlement_price": float,
                                "settlement_type": "settlement"
                            }
                        ]
                    }
                ],
                "current_page": int,
                "total_page": int,
                "total_size": int
            },
            "ts": int
        }

        Schema(schema).validate(r)


if __name__ == '__main__':
    pytest.main()
