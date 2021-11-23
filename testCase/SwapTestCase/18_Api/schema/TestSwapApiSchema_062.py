#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('反向永续')
@allure.feature('api')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_062:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = currentPrice()
        pass

    @classmethod
    def teardown_class(cls):
        pass

    @allure.title("跟踪委托下单")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_track_order(contract_code=contract_code,volume=1,direction='buy',order_price_type='optimal_5',
                                        offset='open',lever_rate=5,active_price=round(self.currentPrice*0.99,2),callback_rate=0.01)
            pass
        schema = {
            "status": "ok",
            "data": {
                "order_id": int,
                "order_id_str": str
            },
            "ts": int
        }
        with allure.step('验证：schema响应字段校验'):
            Schema(schema).validate(r)
            pass
