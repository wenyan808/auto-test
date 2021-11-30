#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_052:

    @allure.title("合约计划委托撤单")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：先挂计划委托单'):
            self.currentPrice = currentPrice()
            orderId = user01.swap_trigger_order(contract_code=contract_code, volume=1,
                                                trigger_price=round(self.currentPrice * 1.01, 2),
                                                order_price=round(self.currentPrice * 0.99, 2), trigger_type="ge",
                                                direction="buy")['data']['order_id']
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(1, 4):
                r = user01.swap_trigger_cancel(contract_code=contract_code, order_id=orderId)
                if r['data']['successes']:
                    flag = True
                    break
                time.sleep(1)
                print('未返回预期结果，第{}次重试………………………………'.format(i))
            assert flag, '重试3次未返回预期结果'
            pass
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
