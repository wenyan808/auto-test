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
class TestSwapApiSchema_026:

    @allure.title("查询用户财务记录")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_financial_record(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "financial_record": [
                        {
                            "id": int,
                            "ts": int,
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "type": int,
                            "amount": Or(float, None),
                        }
                    ],
                    "total_page": int,
                    "current_page": int,
                    "total_size": int
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
