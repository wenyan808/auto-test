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
class TestSwapApiSchema_013:

    @allure.title("查询平台历史结算记录")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_settlement_records(contract_code=contract_code, page_index=1,
                                               page_size=1)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "ts": int,
                "data": {
                    "settlement_record": [
                        {
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "settlement_time": int,
                            "clawback_ratio": Or(float, int, 0),
                            "settlement_price": Or(float, int, 0),
                            "settlement_type": str
                        }
                    ],
                    "current_page": int,
                    "total_page": int,
                    "total_size": int
                }
            }
            Schema(schema).validate(r)
            pass
