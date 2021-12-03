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
class TestSwapApiSchema_039:

    @allure.title("合约批量下单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            self.currentPrice = currentPrice()
            orders_data = {'orders_data':[
                {
                    'contract_code': contract_code,
                    'price': round(self.currentPrice*0.95,2),
                    'volume': 1,
                    'direction': 'buy',
                    'offset': 'open',
                    'lever_rate': 5,
                    'order_price_type': 'limit'
                }, {
                    'contract_code': contract_code,
                    'price': round(self.currentPrice*1.05,2),
                    'volume': 1,
                    'direction': 'sell',
                    'offset': 'open',
                    'lever_rate': 5,
                    'order_price_type': 'limit'
                }
            ]}
            r = user01.swap_batchorder(orders_data=orders_data)
            pass
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
            pass
