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
class TestSwapApiSchema_017:

    @allure.title("批量获取合约的资金费率")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_batch_funding_rate(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data":[
                    {
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "fee_asset": symbol,
                        "funding_time": str,
                        "funding_rate": str,
                        "estimated_rate": str,
                        "next_funding_time": str
                    }],
                "ts": int
            }
            Schema(schema).validate(r)
            pass
