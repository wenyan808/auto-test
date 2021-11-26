#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_051:

    @allure.title("合约计划委托下单")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            self.currentPrice = currentPrice()
            r = user01.swap_trigger_order(contract_code=contract_code, volume=1, trigger_price=round(self.currentPrice*1.01,2),
                                          order_price=round(self.currentPrice*0.99,2), trigger_type="ge", direction="buy")

            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "order_id": int,
                    "order_id_str": str
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
