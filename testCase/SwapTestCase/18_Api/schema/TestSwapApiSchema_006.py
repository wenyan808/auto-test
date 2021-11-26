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
class TestSwapApiSchema_006:

    @allure.title("获取风险准备金历史数据")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_insurance_fund(contract_code=contract_code, page_size=1, page_index=1)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "ts": int,
                "data": {
                    "symbol": symbol,
                    "contract_code": contract_code,
                    "tick": [
                        {
                            "insurance_fund": Or(float, int, 0),
                            "ts": int
                        }
                    ],
                    "total_page": int,
                    "current_page": int,
                    "total_size": int
                }
            }
            Schema(schema).validate(r)
            pass
