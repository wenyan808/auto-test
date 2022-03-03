#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint

import allure
import pytest
import time
from schema import Schema

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_040:

    @allure.title("撤销合约订单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            price = ATP.get_current_price()
            a = user01.swap_order(contract_code=contract_code, price=round(price * 0.8, 2), direction='buy')
            orderid = a['data']['order_id_str']
            time.sleep(1)
            r = user01.swap_cancel(order_id=orderid, contract_code=contract_code)
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "errors": [
                        {
                            "order_id": orderid,
                            "err_code": int,
                            "err_msg": str
                        }
                    ],
                    "successes": orderid
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
