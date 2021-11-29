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
class TestSwapApiSchema_018:

    @allure.title("获取合约的历史资金费率")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_historical_funding_rate(contract_code=contract_code, page_size=1, page_index=1)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "total_page": int,
                    "current_page": int,
                    "total_size": int,
                    "data": [
                        {
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "fee_asset": symbol,
                            "funding_time": str,
                            "funding_rate": str,
                            "realized_rate": str,
                            "avg_premium_index": str,
                        }
                    ]},
                "ts": int
            }
            Schema(schema).validate(r)
            pass