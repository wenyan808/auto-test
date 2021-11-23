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
class TestSwapApiSchema_010:

    @allure.title("精英账户多空持仓对比-账户数")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_elite_account_ratio(contract_code=contract_code, period='1day')
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "list": [{
                            "buy_ratio": Or(float, 0, int, None),
                            "sell_ratio": Or(float, 0, int, None),
                            "locked_ratio": Or(float, 0, int, None),
                            "ts": int
                        }]
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
