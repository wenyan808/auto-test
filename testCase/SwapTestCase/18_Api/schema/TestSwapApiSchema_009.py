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
class TestSwapApiSchema_009:

    @allure.title("获取平台阶梯保证金")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_ladder_margin(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": [{
                    "symbol": symbol,
                    "contract_code": contract_code,
                    "list": [{
                        "lever_rate": int,
                        "ladders": [{
                            "min_margin_balance": Or(int,float,None),
                            "max_margin_balance": Or(int,float,None),
                            "min_margin_available": Or(int,float,None),
                            "max_margin_available": Or(int,float,None)
                        }
                        ]
                    }]
                }],
                "ts": int
            }
            Schema(schema).validate(r)
            pass
