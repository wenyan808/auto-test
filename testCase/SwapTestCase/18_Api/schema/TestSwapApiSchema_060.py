#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01
from common.CommonUtils import currentPrice
from config.conf import DEFAULT_CONTRACT_CODE


@allure.epic('反向永续')
@allure.feature('api')
@allure.story('schema校验')
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
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_tpsl_hisorders(contract_code=contract_code,status=0,create_date=7,page_size=1,page_index=1)
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
