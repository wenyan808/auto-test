#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu
from pprint import pprint

import allure
import pytest
import time
from schema import Schema, Or

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_065:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = ATP.get_current_price()
        cls.orderId = user01.swap_track_order(contract_code=DEFAULT_CONTRACT_CODE, volume=1, direction='buy',
                                              order_price_type='optimal_5',
                                              offset='open', lever_rate=5, active_price=round(cls.currentPrice*0.99, 2),
                                              callback_rate=0.01)['data']['order_id_str']
        pass

    @classmethod
    def teardown_class(cls):
        print(ATP.cancel_all_types_order())
        pass

    @allure.title("获取跟踪委托当前委托")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_track_openorders(contract_code=contract_code, page_size=1, page_index=1, trade_type=0)
                if 'ok' in r['status'] and r['data']['orders']:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i+1}次重试………………………………')
            assert flag, '重试3次未返回预期结果'
            pprint(r)
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "total_page": int,
                    "total_size": int,
                    "current_page": int,
                    "orders": [{
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "volume": Or(float, None, 0, int),
                        "order_type": int,
                        "direction": Or("buy", "sell"),
                        "offset": Or("close", "open"),
                        "lever_rate": int,
                        "order_id": int,
                        "order_id_str": str,
                        "order_source": str,
                        "created_at": int,
                        "order_price_type": str,
                        "status": int,
                        "callback_rate": Or(float, None, 0, int),
                        "active_price": Or(float, None, 0, int),
                        "is_active": Or(0, 1)
                    }]
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
