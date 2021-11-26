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
class TestSwapApiSchema_012:

    @allure.title("获取强平订单")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
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
