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
class TestSwapApiSchema_066:

    @classmethod
    def setup_class(cls):
        cls.currentPrice = SwapTool.currentPrice()
        pass

    @classmethod
    def teardown_class(cls):
        pass

    @allure.title("获取跟踪委托历史委托")
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            flag = False
            # 重试3次未返回预期结果则失败
            for i in range(3):
                r = user01.swap_track_hisorders(contract_code=contract_code, page_size=1, page_index=1, trade_type=0,
                                                status=0, create_date=7)
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
                        "triggered_price": Or(float, int, 0, None),
                        "volume": Or(float, int, 0, None),
                        "order_type": int,
                        "direction": Or("buy", "sell"),
                        "offset": Or("close", "open"),
                        "lever_rate": int,
                        "order_id": int,
                        "order_id_str": str,
                        "order_source": str,
                        "created_at": int,
                        "update_time": int,
                        "order_price_type": str,
                        "status": int,
                        "canceled_at": Or(float, int, 0, None),
                        "fail_code": Or(float, int, 0, None),
                        "fail_reason": Or(float, int, 0, None),
                        "callback_rate": Or(float, int, 0, None),
                        "active_price": Or(float, int, 0, None),
                        "is_active": Or(1, 0),
                        "market_limit_price": Or(float, int, 0, None),
                        "formula_price": Or(float, int, 0, None),
                        "real_volume": int,
                        "relation_order_id": str
                    }]
                },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
