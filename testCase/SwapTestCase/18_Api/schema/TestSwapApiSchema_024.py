#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01


@allure.epic('反向永续')
@allure.feature('18API')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_024:

    @allure.title("查询母账户下的单个子账户资产信息")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_sub_account_info(contract_code=contract_code, sub_uid='115395803')
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": [
                    {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "margin_balance": Or(int, float, 0, None),
                        "margin_position": Or(int, float, 0, None),
                        "margin_frozen": Or(int, float, 0, None),
                        "margin_available": Or(int, float, 0, None),
                        "profit_real": Or(int, float, 0, None),
                        "profit_unreal": Or(int, float, 0, None),
                        "withdraw_available": Or(int, float, 0, None),
                        "risk_rate": Or(int, float, 0, None),
                        "liquidation_price": Or(int, float, 0, None),
                        "adjust_factor": Or(int, float, 0, None),
                        "lever_rate": Or(int, None),
                        "margin_static": Or(int, float, 0, None),
                        "transfer_profit_ratio": Or(int, float, 0, None),
                    }
                ],
                "ts": int
            }

            Schema(schema).validate(r)
            pass
