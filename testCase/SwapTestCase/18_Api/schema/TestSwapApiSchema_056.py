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
class TestSwapApiSchema_056:

    @classmethod
    def setup(self):
        self.currentPrice = ATP.get_current_price()
        user01.swap_order(contract_code=DEFAULT_CONTRACT_CODE, price=self.currentPrice, direction='buy')
        user01.swap_order(contract_code=DEFAULT_CONTRACT_CODE, price=self.currentPrice,direction='sell')


    @classmethod
    def teardown_class(cls):
        with allure.step('撤单'):
            time.sleep(1)
            print(ATP.cancel_all_types_order())
            print(ATP.close_all_position())
            pass

    @allure.title("对仓位设置止盈止损订单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_tpsl_order(contract_code=contract_code, volume=1, direction='sell',
                                           tp_trigger_price=round(self.currentPrice * 1.01, 2),
                                           tp_order_price_type='optimal_5', sl_order_price_type='optimal_5')
                if 'ok' in r['status'] and r['data']['tp_order']:
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
