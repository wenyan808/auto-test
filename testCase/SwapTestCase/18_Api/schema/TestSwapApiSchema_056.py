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
@allure.feature('18API')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_056:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = currentPrice()
        user01.swap_order(contract_code=DEFAULT_CONTRACT_CODE, price=cls.currentPrice, direction='buy')
        user01.swap_order(contract_code=DEFAULT_CONTRACT_CODE, price=cls.currentPrice,direction='sell')


    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @allure.title("对仓位设置止盈止损订单")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_tpsl_order(contract_code=contract_code, volume=1, direction='sell',
                                       tp_trigger_price=round(self.currentPrice * 1.01, 2),
                                       tp_order_price_type='optimal_5',sl_order_price_type='optimal_5')
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "tp_order": Or({
                        "order_id": int,
                        "order_id_str": str
                    },None),
                    "sl_order": Or({
                        "order_id": int,
                        "order_id_str": str
                    },None)
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
