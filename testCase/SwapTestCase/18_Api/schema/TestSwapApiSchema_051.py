#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import allure
import pytest
import time
from schema import Schema

from common.SwapServiceAPI import user01
from config.case_content import epic, features
from config.conf import DEFAULT_CONTRACT_CODE
from tool.atp import ATP


@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_051:

    @classmethod
    def teardown_class(cls):
        with allure.step('恢复环境:取消挂单'):
            time.sleep(1)
            user01.swap_trigger_cancelall(contract_code=DEFAULT_CONTRACT_CODE)
            pass

    @allure.title("合约计划委托下单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                price = ATP.get_current_price()
                r = user01.swap_trigger_order(contract_code=contract_code, volume=1,
                                              trigger_price=round(price * 1.01, 2),
                                              order_price=round(price * 0.99, 2), trigger_type="ge",
                                              direction="buy")
                if 'ok' in r['status'] and r['data']['order_id']:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i + 1}次重试………………………………')
            assert flag, '重试3次未返回预期结果'
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data": {
                    "order_id": int,
                    "order_id_str": str
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
