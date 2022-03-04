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
class TestSwapApiSchema_052:

    @allure.title("合约计划委托撤单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：先挂计划委托单'):
            price = ATP.get_current_price()
            orderId = user01.swap_trigger_order(contract_code=contract_code, volume=1,
                                                trigger_price=round(price * 1.01, 2),
                                                order_price=round(price * 0.99, 2), trigger_type="ge",
                                                direction="buy")['data']['order_id']
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_trigger_cancel(contract_code=contract_code, order_id=orderId)
                if 'ok' in r['status'] and r['data']['successes']:
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
                    "errors": [],
                    "successes": str(orderId)
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
