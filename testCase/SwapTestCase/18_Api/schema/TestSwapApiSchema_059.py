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
class TestSwapApiSchema_059:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = SwapTool.currentPrice()

    @classmethod
    def teardown_class(cls):
        time.sleep(1)
        user01.swap_tpsl_cancelall(contract_code=DEFAULT_CONTRACT_CODE)
        pass

    @allure.title("获取止盈止损当前委托")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：挂单'):
            user01.swap_tpsl_order(contract_code=contract_code, volume=1, direction='sell',
                                   tp_trigger_price=round(self.currentPrice * 1.01, 2),
                                   tp_order_price_type='optimal_5', sl_order_price_type='optimal_5')
            pass
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_tpsl_openorders(contract_code=contract_code)
                if 'ok' in r['status'] and r['data']['orders']:
                    flag = True
                    break
                time.sleep(1)
                print(f'未返回预期结果，第{i+1}次重试………………………………')
            assert flag, '重试3次未返回预期结果'
            pass
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
                        "volume": Or(float, int, 0, None),
                        "order_type": int,
                        "tpsl_order_type": str,
                        "direction": Or("buy", "sell"),
                        "order_id": int,
                        "order_id_str": str,
                        "order_source": str,
                        "order_price": Or(float, int, 0, None),
                        "trigger_type": Or("ge", "le"),
                        "trigger_price": Or(float, int, 0, None),
                        "created_at": int,
                        "order_price_type": str,
                        "status": int,
                        "source_order_id": Or(str,None),
                        "relation_tpsl_order_id": str
                    }]
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
