#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice


@allure.epic('反向永续')
@allure.feature('api')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_041:

    @allure.title("撤销全部合约单")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            self.currentPrice = currentPrice()
            user01.swap_order(contract_code=contract_code,price=round(self.currentPrice*0.5,2),direction='buy')
            time.sleep(1)
            r = user01.swap_cancelall(contract_code=contract_code)
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "errors": [
                        {
                            "order_id": str,
                            "err_code": int,
                            "err_msg": str
                        }
                    ],
                    "successes": str
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
