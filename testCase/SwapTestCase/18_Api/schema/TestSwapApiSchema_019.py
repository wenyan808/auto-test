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
class TestSwapApiSchema_019:

    @allure.title("获取用户的合约账户信息")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_account_info(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": [
                    {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "margin_balance": Or(int, float, 0, None),
                        "margin_static": Or(int, float, 0, None),
                        "margin_position": Or(int, float, 0, None),
                        "margin_frozen": Or(int, float, 0, None),
                        "margin_available": Or(int, float, 0, None),
                        "profit_real": Or(int, float, 0, None),
                        "profit_unreal": Or(int, float, 0, None),
                        "withdraw_available": Or(int, float, 0, None),
                        "risk_rate": Or(int, float, 0, None),
                        "liquidation_price": Or(int, float, 0, None),
                        "lever_rate": int,
                        "adjust_factor": Or(int, float, 0, None),
                        "transfer_profit_ratio":Or(int, float, 0, None)
                    }
                ],
                "ts": int
            }
            Schema(schema).validate(r)
            pass
