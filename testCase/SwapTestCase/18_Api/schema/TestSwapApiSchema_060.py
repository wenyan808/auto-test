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
class TestSwapApiSchema_060:

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    @allure.title("查询止盈止损订单历史委托")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_tpsl_hisorders(contract_code=contract_code,status=0,create_date=7,page_size=1,page_index=1)
                if 'ok' in r['status'] and r['data']['orders']:
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
                    "total_page": int,
                    "total_size": int,
                    "current_page": int,
                    "orders": [{
                        "symbol": symbol,
                        "contract_code": contract_code,
                        "volume": Or(float, None, int, 0),
                        "order_type": int,
                        "direction": Or("buy", "sell"),
                        "tpsl_order_type": str,
                        "order_id": int,
                        "order_id_str": str,
                        "order_source": str,
                        "order_price": Or(float, None, int, 0),
                        "created_at": int,
                        "order_price_type": str,
                        "trigger_type": Or("ge", "le"),
                        "trigger_price": Or(float,None,int,0),
                        "status": int,
                        "source_order_id": Or(str,None),
                        "relation_tpsl_order_id": str,
                        "canceled_at": Or(float, None, int, 0),
                        "fail_code": Or(float, None, int, 0),
                        "fail_reason": Or(float, None, int, 0),
                        "triggered_price": Or(float, None, int, 0),
                        "relation_order_id": str,
                        "update_time": int
                    }]
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
