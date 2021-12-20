#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

from common.mysqlComm import mysqlComm as mysqlClient

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from tool.SwapTools import SwapTool
from config.conf import DEFAULT_CONTRACT_CODE
from config.case_content import epic,features

@allure.epic(epic[1])
@allure.feature(features[17]['feature'])
@allure.story(features[17]['story'][1])
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_057:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = currentPrice()

    @classmethod
    def teardown_class(cls):
        with allure.step(''):
            pass

    @allure.title("止盈止损订单撤单")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：挂单'):
            orderInfo = user01.swap_tpsl_order(contract_code=contract_code, volume=1, direction='sell',
                                             tp_trigger_price=round(self.currentPrice * 1.01, 2),
                                             tp_order_price_type='optimal_5', sl_order_price_type='optimal_5')
            orderId = orderInfo['data']['tp_order']['order_id_str']
            pass
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_tpsl_cancel(contract_code=contract_code, order_id=orderId)
                if 'ok' in r['status'] and r['data']['successes']:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i+1}次重试………………………………')
            assert flag, '重试3次未返回预期结果'
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                'status': 'ok',
                'ts': int,
                'data': {
                    'errors': [{
                        'err_code': int,
                        'err_msg': str,
                        'order_id': str
                    }],
                    'successes': str
                }
            }
            Schema(schema).validate(r)
            pass
