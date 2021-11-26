#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_040:

    @allure.title("撤销合约订单")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            self.currentPrice = currentPrice()
            orderId = user01.swap_order(contract_code=contract_code,price=round(self.currentPrice*0.5,2),direction='buy')['data']['order_id_str']
            time.sleep(1)
            r = user01.swap_cancel(order_id=orderId,contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "errors": [
                        {
                            "order_id": orderId,
                            "err_code": int,
                            "err_msg": str
                        }
                    ],
                    "successes": orderId
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
