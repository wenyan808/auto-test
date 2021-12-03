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
class TestSwapApiSchema_012:

    @allure.title("获取强平订单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_liquidation_orders(contract_code=contract_code, trade_type=0, create_date=7, page_index=1,
                                               page_size=1)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "orders": [
                        {
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "direction": symbol,
                            "offset": str,
                            "volume": Or(int,float,0,None),
                            "price": Or(int,float,0,None),
                            "created_at": int,
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
