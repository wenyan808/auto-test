#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint

import allure
import pytest
from schema import Schema, Or

from common.SwapServiceAPI import user01
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_013:

    @allure.title("查询平台历史结算记录")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_settlement_records(contract_code=contract_code, page_index=1,
                                               page_size=1)
            pprint(r)
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
