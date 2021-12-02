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
class TestSwapApiSchema_055:

    @allure.title("获取计划委托历史委托")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_trigger_hisorders(contract_code=contract_code, trade_type=0, create_date=7, status=0,
                                                  page_size=1, page_index=1)
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
                    "orders": [
                        {
                            "symbol": symbol,
                            "contract_code": contract_code,
                            "trigger_type": Or("ge", "le"),
                            "volume": Or(float, int, 0, None),
                            "order_type": int,
                            "direction": Or("sell", "buy"),
                            "offset": Or("open", "close"),
                            "lever_rate": int,
                            "order_id": int,
                            "order_id_str": str,
                            "relation_order_id": str,
                            "order_price_type": str,
                            "status": int,
                            "order_source": str,
                            "trigger_price": Or(float, int, 0, None),
                            "triggered_price": Or(float, int, 0, None),
                            "order_price": Or(float, int, 0, None),
                            "created_at": int,
                            "triggered_at":  Or(float, int, 0, None),
                            "order_insert_at": int,
                            "canceled_at": int,
                            "fail_code": Or(float, int, 0, None),
                            "fail_reason": Or(float, int, 0, None),
                            "update_time": int
                        }
                    ],
                    "total_page": int,
                    "current_page": int,
                    "total_size": int
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
