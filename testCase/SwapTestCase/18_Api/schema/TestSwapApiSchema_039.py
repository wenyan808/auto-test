#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint
from time import sleep

import allure
import pytest
from schema import Schema

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_039:

    @allure.title("合约批量下单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            price = ATP.get_current_price()
            orders_data = {'orders_data':[
                {
                    'contract_code': contract_code,
                    'price': round(price*0.95,2),
                    'volume': 1,
                    'direction': 'buy',
                    'offset': 'open',
                    'lever_rate': 5,
                    'order_price_type': 'limit'
                }, {
                    'contract_code': contract_code,
                    'price': round(price*1.05,2),
                    'volume': 1,
                    'direction': 'sell',
                    'offset': 'open',
                    'lever_rate': 5,
                    'order_price_type': 'limit'
                }
            ]}
            r = user01.swap_batchorder(orders_data=orders_data)
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "errors": [
                        {
                            "index": int,
                            "err_code": int,
                            "err_msg": str
                        }
                    ],
                    "success": [
                        {
                            "index": int,
                            "order_id": int,
                            "order_id_str": str
                        }
                    ]
                },
                "ts": int
            }
            Schema(schema).validate(r)

    @allure.step('恢复环境')
    def teardown(self):
        print('\n恢复环境操作')
        sleep(2)
        print(ATP.cancel_all_order())
