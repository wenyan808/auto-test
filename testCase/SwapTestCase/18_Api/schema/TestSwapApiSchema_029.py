#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint

import allure
import pytest
from schema import Schema

from common.SwapServiceAPI import user01
from config.case_content import epic, features


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_029:

    @allure.title("获取用户的合约下单量限制")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_order_limit(contract_code=contract_code,order_price_type='limit')
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "order_price_type": "limit",
                    "list": [
                        {
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "open_limit": float,
                            "close_limit": float
                        }
                    ]
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
