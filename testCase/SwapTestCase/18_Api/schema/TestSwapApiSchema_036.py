#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2021/11/22 10:55 上午
# @Author  : HuiQing Yu

import pytest, allure, random, time
from schema import Schema, Or
from common.SwapServiceAPI import user01


@allure.epic('反向永续')
@allure.feature('18API')
@allure.story('schema校验')
@allure.tag('Script owner : 余辉青', 'Case owner : 张让翰')
@pytest.mark.stable
class TestSwapApiSchema_036:

    @allure.title("新增获取用户API指标禁用信息")
    @pytest.mark.flaky(reruns=1, reruns_delay=1)
    def test_execute(self, symbol, contract_code):
        with allure.step('操作：执行api'):
            r = user01.swap_api_trading_status()
            pass
        with allure.step('验证：schema响应字段校验'):
            schema = {
                "status": "ok",
                "data":
                    {
                        "is_disable": Or(1,0),
                        "order_price_types": str,
                        "disable_reason": str,
                        "disable_interval": int,
                        "recovery_time": int,
                        "COR":
                            {
                                "orders_threshold": int,
                                "orders": int,
                                "invalid_cancel_orders": int,
                                "cancel_ratio_threshold": Or(float,0),
                                "cancel_ratio": Or(float,0),
                                "is_trigger": Or(1,0),
                                "is_active": Or(1,0)
                            },
                        "TDN":
                            {
                                "disables_threshold": int,
                                "disables": int,
                                "is_trigger": Or(1,0),
                                "is_active": Or(1,0)
                            }
                    },
                "ts": int
            }
            Schema(schema).validate(r)
            pass
