#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01


@allure.epic('反向永续')
@allure.feature('api')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_033:

    @allure.title("获取用户资产和持仓信息")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_account_position_info(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "ts": int,
                "data": [{
                    "symbol": symbol,
                    "contract_code": contract_code,
                    "margin_balance": Or(float, int, 0),
                    "margin_position": Or(float, int, 0),
                    "margin_frozen": Or(float, int, 0),
                    "margin_available": Or(float, int, 0),
                    "profit_real": Or(float, int, 0),
                    "profit_unreal": Or(float, int, 0),
                    "risk_rate": Or(float, int, 0, None),
                    "withdraw_available": Or(float, int, 0, None),
                    "liquidation_price": Or(float, int, 0, None),
                    "lever_rate": Or(float, int, 0, None),
                    "adjust_factor": Or(float, int, 0, None),
                    "margin_static": Or(float, int, 0, None),
                    "positions": [{
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "volume": Or(float, int, 0, None),
                        "available": Or(float, int, 0, None),
                        "frozen": Or(float, int, 0, None),
                        "cost_open": Or(float, int, 0, None),
                        "cost_hold": Or(float, int, 0, None),
                        "profit_unreal": Or(float, int, 0, None),
                        "profit_rate": Or(float, int, 0, None),
                        "profit": Or(float, int, 0, None),
                        "position_margin": Or(float, int, 0, None),
                        "lever_rate": Or(float, int, 0, None),
                        "direction": Or('buy', 'sell'),
                        "last_price": Or(float, int, 0, None),
                    }]
                }]
            }
            Schema(schema).validate(r)
            pass
