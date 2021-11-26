#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_028:

    @allure.title("查询用户结算记录")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_user_settlement_records(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "total_page": int,
                    "current_page": int,
                    "total_size": int,
                    "settlement_records": [
                        {
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "margin_balance_init": Or(int, float, 0, None),
                            "margin_balance": Or(int, float, 0, None),
                            "settlement_profit_real": Or(int, float, 0, None),
                            "settlement_time": Or(int, float, 0, None),
                            "clawback": Or(int, float, 0, None),
                            "funding_fee": Or(int, float, 0, None),
                            "offset_profitloss": Or(int, float, 0, None),
                            "fee": Or(int, float, 0, None),
                            "fee_asset": symbol,
                            "positions": [
                                {
                                    "symbol": symbol,
                                    "contract_code": contract_code,
                                    "direction": Or('buy', 'sell'),
                                    "volume": Or(int, float, 0, None),
                                    "cost_open": Or(int, float, 0, None),
                                    "cost_hold_pre": Or(int, float, 0, None),
                                    "cost_hold": Or(int, float, 0, None),
                                    "settlement_profit_unreal": Or(int, float, 0, None),
                                    "settlement_price": Or(int, float, 0, None),
                                    "settlement_type": "settlement"
                                }
                            ]
                        }
                    ]
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
